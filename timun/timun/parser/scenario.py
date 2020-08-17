from typing import List
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


setattr(parse_scenario_like, "__PARSER__", "scenario-like")

parse_scenario: Parser[Scenario] = lambda input: parse_scenario_like(
    input, ScenarioType.SCENARIO
)

setattr(parse_scenario, "__PARSER__", "scenario")

parse_fail_scenario: Parser[Scenario] = lambda input: parse_scenario_like(
    input, ScenarioType.FAIL_SCENARIO
)

setattr(parse_fail_scenario, "__PARSER__", "fail scenario")

parse_scenario_family = parser_or(parse_scenario, parse_fail_scenario)

# parse_scenarios: Parser[List[Scenario]] = one_or_more(parse_scenario)
parse_scenarios: Parser[List[Scenario]] = one_or_more(parse_scenario_family)
