import traceback
from typing import List, Dict, Optional
from dataclasses import dataclass


from timun.model import Feature, Scenario, ScenarioOutline, ScenarioType, Step
from timun.step import StepDescriptor
from termcolor import colored


@dataclass
class ScenarioTestReport:
    feature: Feature
    scenario: Scenario
    fail_step: Optional[Step] = None
    exception: Optional[Exception] = None
    step_desc: Optional[StepDescriptor] = None
    message: Optional[str] = None
    show_traceback = True

    def desc_line(self) -> str:
        res = f"{colored(self.scenario.keyword.name, 'blue')}\t: {self.scenario.text}"
        res += f"@{self.feature.filename}:{self.scenario.idx + 1} - "
        if self.exception:
            res += f"{colored('FAILED', 'red')}:"
        else:
            res += colored("SUCCESS", "green")
        return res

    def __str__(self) -> str:
        res = self.desc_line()
        if self.exception:
            if self.fail_step:
                f"\n\tStep: {self.fail_step.text}:{self.fail_step.idx}"

            if self.step_desc:
                res += f" (desc {self.step_desc.function.__name__}"
                res += f"@{self.step_desc.filename}:{self.step_desc.function.__code__.co_firstlineno})"

            if self.message == None:
                self.message = "\n".join(self.exception.args)

        if self.message:
            lines = self.message.splitlines()
            if self.show_traceback and not isinstance(self.exception, AssertionError):
                for l in lines[:-1]:
                    res += f"\n\t| {l}"
            res += f"\n\t| {lines[-1]}"

        return res


class TestRunner:
    def __init__(self, features: List[Feature], step_dict: Dict[str, StepDescriptor]):
        self.features = features
        self.step_dict = step_dict
        self._indent = 0

        self.test_report: List[ScenarioTestReport] = []

    def run(self):
        self.test_report = []
        for feature in self.features:
            self.run_feature(feature)

        print("==== Failed Scenarios ====")
        for report in self.test_report:
            if report.exception != None:
                print(report)

    def run_feature(self, feature: Feature):
        print(f"==== Feature: {feature.text} @ {feature.filename}:{feature.idx+1}")

        for scenario in feature.scenarios:
            if isinstance(scenario, ScenarioOutline):
                raise Exception(
                    f"Unexpanded scenario outline ({feature.filename}:{scenario.idx+1})"
                )

            self.run_scenario(feature, scenario)

    def run_scenario(self, feature: Feature, scenario: Scenario):
        context = {"failed": False}

        report = ScenarioTestReport(feature, scenario)

        scenario_type = scenario.keyword

        if scenario_type == ScenarioType.FAIL_SCENARIO:
            try:
                for step in scenario.steps:
                    self.run_step(step, context)

                report.exception = Exception(
                    "All test in this scenario passes, expected failure"
                )
            except Exception as e:
                pass
        else:
            # NORMAL SCENARIO CASE
            for step in scenario.steps:
                try:
                    self.run_step(step, context)
                except Exception as e:
                    report.fail_step = step
                    report.exception = e
                    try:
                        report.step_desc, _ = self.find_matching_step(step)
                    except:
                        report.step_desc = None
                        report.show_traceback = False
                    report.message = traceback.format_exc().strip()
                    break

        print(report.desc_line())
        self.test_report.append(report)

    def run_step(self, step: Step, context):
        step_definition, match = self.find_matching_step(step)
        step_definition.function(context, **match.named)

    def find_matching_step(self, step: Step):
        matching_step: List[StepDescriptor] = []

        # find matching step descriptor
        for desc in self.step_dict.values():
            match = desc.pattern.parse(step.text)
            if match:
                matching_step.append(desc)

        if matching_step == []:
            raise Exception(f"Can't find matching step definition for '{step.text}'")

        # TODO: Raise exception when multiple matching steps found

        return matching_step[0], matching_step[0].pattern.parse(step.text)

