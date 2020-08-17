from typing import List

from parse import parse
from timun.model import Scenario, ScenarioType
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
from . import parser


@parser("scenario-like")
def parse_scenario_like(
    input: ParserInput, expect_type: ScenarioType
) -> ParserResult[Scenario]:

    cur_line, cur_idx, next_input = next_nonempty_line(input)
    head, _, rest = cur_line.partition(":")
    head = head.strip().lower()
    rest = rest.strip()

    type = ScenarioType.from_string(head)

    if type and type == expect_type:
        steps, next_input = parse_steps(next_input)

        scenario = Scenario(type, rest, steps, cur_idx)
        return scenario, next_input

    raise ParserError(
        f"expected '{expect_type.name.lower()}' found '{cur_line}''", input
    )


parse_scenario: Parser[Scenario] = parser("scenario")(
    lambda input: parse_scenario_like(input, ScenarioType.SCENARIO)
)

parse_fail_scenario: Parser[Scenario] = parser("fail scenario")(
    lambda input: parse_scenario_like(input, ScenarioType.FAIL_SCENARIO)
)

parse_scenario_family = parser("scenario-family")(
    parser_or(parse_scenario, parse_fail_scenario)
)

parse_scenarios: Parser[List[Scenario]] = parser("scenarions")(
    one_or_more(parse_scenario_family)
)
