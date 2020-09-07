from timun.parser.table import (
    parse_table_example,
    parse_table_fail_example,
    parse_table_variable_accepted,
    parse_table_variable_rejected,
    parse_tables_outline,
)
from typing import List, Optional, Tuple

from timun.model import Scenario, ScenarioOutline, ScenarioType, Table
from .combinator import (
    Parser,
    ParserInput,
    ParserError,
    ParserResult,
    next_nonempty_line,
    parser_or,
    one_or_more,
)
from .step import parse_steps
from .decorator import parser


def parse_variable_tables(
    input: ParserInput,
) -> ParserResult[Tuple[Optional[Table], Optional[Table]]]:
    try:
        variable_accepted_table, input = parse_table_variable_accepted(input)
    except ParserError as p:
        variable_accepted_table = None

    try:
        variable_rejected_table, input = parse_table_variable_rejected(input)
    except ParserError as p:
        variable_rejected_table = None

    return (variable_accepted_table, variable_rejected_table), input


@parser("scenario-like")
def parse_scenario_like(
    input: ParserInput, expect_type: ScenarioType
) -> ParserResult[Scenario]:

    cur_line, cur_idx, next_input = next_nonempty_line(input)
    head, _, rest = cur_line.partition(":")
    head = head.strip().lower()
    rest = rest.strip()

    type = ScenarioType.from_string(head)

    if type != expect_type:
        raise ParserError(
            f"expected '{expect_type.name.lower()}' found '{cur_line}''", input
        )

    steps, next_input = parse_steps(next_input)

    (
        (variable_accepted_table, variable_rejected_table),
        next_input,
    ) = parse_variable_tables(next_input)

    scenario = Scenario(
        type, rest, steps, cur_idx, variable_accepted_table, variable_rejected_table
    )
    return scenario, next_input


parse_scenario: Parser[Scenario] = parser("scenario")(
    lambda input: parse_scenario_like(input, ScenarioType.SCENARIO)
)

parse_fail_scenario: Parser[Scenario] = parser("fail scenario")(
    lambda input: parse_scenario_like(input, ScenarioType.FAIL_SCENARIO)
)


@parser("scenario outline")
def parse_scenario_outline(input: ParserInput) -> ParserResult[ScenarioOutline]:
    cur_line, cur_idx, next_input = next_nonempty_line(input)
    head, _, rest = cur_line.partition(":")
    head = head.strip().lower()
    rest = rest.strip()

    if head != "scenario outline":
        raise ParserError(f"Expected 'scenario outline' found '{head}'", input)

    steps, next_input = parse_steps(next_input)

    try:
        example_table, next_input = parse_table_example(next_input)
    except ParserError as e:
        example_table = None

    try:
        fail_example_table, next_input = parse_table_fail_example(next_input)
    except ParserError as e:
        fail_example_table = None

    if example_table == None and fail_example_table == None:
        raise ParserError(f"Scenario outline expects example or fail example", input)
    # (
    #     (variable_accepted_table, variable_rejected_table),
    #     next_input,
    # ) = parse_variable_tables(next_input)

    return (
        ScenarioOutline(
            rest,
            steps,
            example_table,
            fail_example_table,
            cur_idx,
            # variable_accepted_table,
            # variable_rejected_table,
        ),
        next_input,
    )


parse_scenario_family = parser("scenario-family")(
    parser_or(parse_scenario, parse_fail_scenario, parse_scenario_outline)
)

parse_scenarios = parser("scenarions")(one_or_more(parse_scenario_family))
