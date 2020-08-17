from typing import List, Optional
from .combinator import (
    ParserResult,
    ParserError,
    Parser,
    ParserInput,
    one_or_more,
    next_nonempty_line,
)
from timun.model import Feature, Scenario, ScenarioType

from .scenario import parse_scenario_like, parse_scenarios
from . import parser


@parser("feature")
def parse_feature(input: ParserInput) -> ParserResult[Feature]:
    tags: List[str] = []

    cur_line, cur_idx, next_input = next_nonempty_line(input)
    head, _, rest = cur_line.partition(":")
    head = head.strip().lower()
    rest = rest.strip()

    if head != "feature":
        raise ParserError(f"expected feature but found '{cur_line}'", input)

    background: Optional[Scenario] = None

    try:
        background, next_input = parse_scenario_like(
            next_input, ScenarioType.BACKGROUND
        )
    except ParserError:
        pass

    scenarios, next_input = parse_scenarios(next_input)

    feature = Feature(tags, rest, background, scenarios, cur_idx, input.filename)

    return feature, next_input


parse_features = one_or_more(parse_feature)
