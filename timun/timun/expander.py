from itertools import product
from re import error
from timun.parser import scenario
from typing import List, Optional, Tuple, Union, cast
from timun.model import (
    Scenario,
    ScenarioOutline,
    Feature,
    ScenarioType,
    Step,
    Table,
    TableEntry,
    VariableDeclaration,
)
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

    example_scenario = expand_scenario_outline_example(scenario, scenario.example_table)
    res += example_scenario

    fail_example_scenario = expand_scenario_outline_example(
        scenario, scenario.fail_example_table
    )
    res += fail_example_scenario

    return res


def expand_scenario_outline_example(
    scenario: Union[ScenarioOutline, Scenario], table: Optional[Table]
) -> List[Scenario]:
    res: List[Scenario] = []

    if table == None:
        return res

    table = cast(Table, table)
    table_type, table_body = table

    table_header = table_body[0]
    table_entries = table_body[1:]

    if isinstance(scenario, ScenarioOutline):
        scenario_type = ScenarioType.SCENARIO
        if table_type in ["fail example", "variable rejected"]:
            scenario_type = ScenarioType.FAIL_SCENARIO
    else:
        scenario_type = scenario.type
        if table_type in ["fail example", "variable rejected"]:
            scenario_type = scenario.type.invert()

    if isinstance(scenario, Scenario):
        var_acc = None
        var_rej = None
    else:
        var_acc = scenario.variable_accepted
        var_rej = scenario.variable_rejected

    steps = scenario.steps
    for entry in table_entries:
        replaced_steps = replace_steps_template(steps, table_header, entry)

        outline_name = " ("
        outline_name += ", ".join([f"{v[0]}={v[1]}" for v in zip(table_header, entry)])
        outline_name += ")"

        new_scenario = Scenario(
            scenario_type,
            scenario.text + outline_name,
            replaced_steps,
            scenario.idx,
            var_acc,
            var_rej,
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
    text = step.text

    for k in repl_dict.keys():
        text = text.replace(f"<{k}>", "{" + k + "}")

    text = text.format(**repl_dict)
    step.text = text

    return step


def expand_variables_feature(
    variable: VariableDeclaration, feature: Feature
) -> Feature:
    expanded_scenarios: List[Scenario] = []

    for scenario in feature.scenarios:
        if not isinstance(scenario, Scenario):
            exit(1)

        if scenario.variable_accepted == None and scenario.variable_rejected == None:
            res = [scenario]
        else:
            res = expand_variable_scenario(variable, scenario)

        expanded_scenarios += res

    feature = copy(feature)
    feature.scenarios = list(expanded_scenarios)

    return feature


def expand_variable_scenario(
    variable: VariableDeclaration, scenario: Scenario
) -> List[Scenario]:
    res: List[Scenario] = []

    gen_tables: List[Table] = []

    # build table
    if scenario.variable_accepted:
        gen_tables += variable_generate_table(variable, scenario.variable_accepted)

    if scenario.variable_rejected:
        gen_tables += variable_generate_table(variable, scenario.variable_rejected)

    for table in gen_tables:
        res += expand_scenario_outline_example(scenario, table)

    #     gen_scenario = expand_scenario_outline_example(scenario, gen_table)
    #     res += gen_scenario

    # res.append(scenario)

    return res


def variable_generate_table(
    variable: VariableDeclaration, table: Table
) -> Tuple[Table, Table]:
    table_name, t = table
    table_head, table_values = t[0], t[1:]

    to_product = []

    for var in table_head:
        if var not in variable.var_dict.keys():
            print(f"Undeclared variable '{var}'")
            exit(1)

        to_product.append(variable.var_dict[var].values)

    values_uni: List[TableEntry] = [list(x) for x in product(*to_product)]

    pos_values = table_values
    pos_table: Table = (table_name, [table_head, *pos_values])

    neg_values = []
    for val in values_uni:
        if val not in pos_values:
            neg_values.append(val)

    if table_name == "variable accepted":
        table_name = "variable rejected"
    else:
        table_name = "variable accepted"

    neg_table = (table_name, [table_head, *neg_values])

    return pos_table, neg_table
