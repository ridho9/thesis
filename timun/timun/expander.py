from timun.parser import scenario
from typing import List
from timun.model import Scenario, ScenarioOutline, Feature, ScenarioType, Step
from copy import copy


def expand_feature(feature: Feature) -> Feature:
    expanded_scenario = []

    for scenario in feature.scenarios:
        if isinstance(scenario, Scenario):
            expanded_scenario.append(scenario)
            continue

        res = expand_scenario_outline(scenario)
        for s in res:
            expanded_scenario.append(s)

    feature = copy(feature)
    feature.scenarios = list(expanded_scenario)

    return feature


def expand_scenario_outline(scenario: ScenarioOutline) -> List[Scenario]:
    res: List[Scenario] = []

    for table in scenario.tables:
        section_header = table[0]
        table_header = table[1][0]
        table_entries = table[1][1:]

        scenario_type = ScenarioType.SCENARIO
        if section_header == "fail example":
            scenario_type = ScenarioType.FAIL_SCENARIO

        steps = scenario.steps
        for entry in table_entries:
            replaced_steps = replace_steps_template(steps, table_header, entry)

            outline_name = "("
            outline_name += ", ".join(
                [f"{v[0]}={v[1]}" for v in zip(table_header, entry)]
            )
            outline_name += ")"

            new_scenario = Scenario(
                scenario_type,
                scenario.text + outline_name,
                replaced_steps,
                scenario.idx,
            )

            res.append(new_scenario)

    return res


def replace_steps_template(
    steps: List[Step], header: List[str], value: List[str]
) -> List[Step]:
    repl_dict = dict()

    for key, val in zip(header, value):
        repl_dict[key] = val

    f = lambda step: replace_step_template(step, repl_dict)

    return list(map(f, steps))


def replace_step_template(step: Step, repl_dict: dict) -> Step:
    step = copy(step)

    text = step.text.replace("<", "{").replace(">", "}")
    text = text.format(**repl_dict)
    step.text = text

    return step
