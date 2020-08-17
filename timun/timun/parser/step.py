from .combinator import (
    ParserInput,
    ParserResult,
    next_nonempty_line,
    ParserError,
    one_or_more,
)

from timun.model import Step, StepType
from . import parser


@parser("step")
def parse_step(input: ParserInput) -> ParserResult[Step]:
    cur_line, cur_idx, next_input = next_nonempty_line(input)
    head, _, rest = cur_line.partition(" ")
    rest = rest.strip()
    type = StepType.from_string(head)

    if type:
        return Step(type, rest.strip(), cur_idx), next_input

    raise ParserError(f"expected step keyword found '{cur_line}'", input)


parse_steps = parser("steps")(one_or_more(parse_step))
