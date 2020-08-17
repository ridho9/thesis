from .combinator import (
    ParserInput,
    ParserResult,
    next_nonempty_line,
    ParserError,
    one_or_more,
)

from timun.model import Step, StepType


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
