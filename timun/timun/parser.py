from timun.step import then
from typing import Tuple, List, Callable, TypeVar, Optional
from dataclasses import dataclass
from timun.model import Step, StepType, Scenario, ScenarioType, Feature
from collections import namedtuple


ParserInput: Tuple[List[str], int, str] = namedtuple(
    "ParserInput", ["lines", "idx", "filename"]
)

T = TypeVar("T")
ParserResult = Tuple[T, ParserInput]
Parser = Callable[[ParserInput], ParserResult[T]]


class ParserError(Exception):
    def __init__(self, message: str, input: ParserInput):
        self.message = f"{message} [{input.filename}:{input.idx+1}]"
        super().__init__(self.message)


def create_input(filename: str, content: str) -> ParserInput:
    return ParserInput(content.splitlines(), 0, filename)


def next_line(input: ParserInput) -> Tuple[str, int, ParserInput]:
    if input.lines == []:
        raise ParserError("unexpected EOF", input)

    head_line, rest_lines = input[0][0], input[0][1:]
    next_idx = input.idx + 1
    return (
        head_line.strip(),
        input.idx,
        ParserInput(rest_lines, input.idx + 1, input.filename),
    )


def next_nonempty_line(input: ParserInput) -> Tuple[str, int, ParserInput]:
    while True:
        line, idx, next_input = next_line(input)
        line = line.strip()
        if line != "":
            return line, idx, next_input
        input = next_input


def zero_or_more(parser: Parser[T]) -> Parser[List[T]]:
    def f(input: ParserInput) -> ParserResult[List[T]]:
        res = []
        while True:
            try:
                val, next_input = parser(input)
                res.append(val)
                input = next_input
            except ParserError:
                break
        return res, input

    return f


def one_or_more(parser: Parser[T]) -> Parser[List[T]]:
    def f(input: ParserInput) -> ParserResult[List[T]]:
        res, next_input = zero_or_more(parser)(input)
        if res != []:
            return res, next_input
        raise ParserError(f"expected one or more '{parser.__PARSER__}'", input)  # type: ignore

    return f


def parser_or(*parsers: Parser) -> Parser:
    desc_line = " or ".join([p.__PARSER__ for p in parsers])  # type: ignore

    def f(input: ParserInput) -> ParserResult:
        for parser in parsers:
            try:
                result = parser(input)
                return result
            except ParserError as p:
                continue

        raise ParserError(f"expected one of {desc_line}", input)

    setattr(f, "__PARSER__", desc_line)

    return f


# ========= PARSER DEFINITION =================


def parse_step(input: ParserInput) -> ParserResult[Step]:

    cur_line, cur_idx, next_input = next_nonempty_line(input)
    head, _, rest = cur_line.partition(" ")
    rest = rest.strip()
    type = StepType.from_string(head)

    if type:
        return Step(type, rest.strip(), cur_idx), next_input

    raise ParserError(f"expected step keyword found '{cur_line}'", input)


setattr(parse_step, "__PARSER__", "step")

parse_steps = one_or_more(parse_step)


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


setattr(parse_step, "__PARSER__", "scenario-like")

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
