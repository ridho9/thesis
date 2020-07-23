import traceback
from typing import List, Dict, Optional
from dataclasses import dataclass


from timun.model import Feature, Scenario, Step
from timun.step import StepDescriptor
from termcolor import colored


class ScenarioRunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


@dataclass
class ScenarioTestReport:
    feature: Feature
    scenario: Scenario
    fail_step: Optional[Step] = None
    exception: Optional[Exception] = None
    step_desc: Optional[StepDescriptor] = None
    traceback: Optional[str] = None

    def __str__(self) -> str:
        res = f"{colored('Scenario', 'blue')}: {self.scenario.text}"
        res += f"@{self.feature.filename}:{self.scenario.idx + 1} - "
        if self.fail_step and self.step_desc and self.traceback:
            res += (
                f"{colored('FAILED', 'red')}:\n\t"
                f"Step: {self.fail_step.text}:{self.fail_step.idx}"
                f" (desc {self.step_desc.function.__name__}"
                f"@{self.step_desc.filename}:{self.step_desc.function.__code__.co_firstlineno})"
            )
            for l in self.traceback.splitlines():
                res += f"\n\t| {l}"
        else:
            res += colored("SUCCESS", "green")

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
            if report.fail_step != None:
                print(report)

    def run_feature(self, feature: Feature):
        print(f"==== Feature: {feature.text} @ {feature.filename}:{feature.idx+1}")

        for scenario in feature.scenarios:
            self.run_scenario(feature, scenario)

    def run_scenario(self, feature: Feature, scenario: Scenario):
        context = {"failed": False}

        report = ScenarioTestReport(feature, scenario)

        for step in scenario.steps:
            try:
                self.run_step(step, context)
            except Exception as e:
                report.fail_step = step
                report.exception = e
                report.step_desc = self.find_matching_step(step)
                report.traceback = traceback.format_exc().strip()
                break

        print(report)
        self.test_report.append(report)

    def run_step(self, step: Step, context):
        step_definition = self.find_matching_step(step)
        step_definition.function(context)

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

        return matching_step[0]

