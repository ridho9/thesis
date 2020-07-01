from typing import Tuple, Optional, List, Callable, TypeVar

from timun.model import *

ParserInput = str

T = TypeVar("T")
Result = Tuple[T, ParserInput]

TParser = Callable[[ParserInput], Result[T]]
SingleParser = TParser[Optional[T]]
MultipleParser = TParser[List[T]]


def create_parse_multiple(single_parser: SingleParser[T]) -> MultipleParser[T]:
    def f(input: str):
        result = []
        while True:
            (step, input) = single_parser(input)
            if step is not None:
                result.append(step)
            else:
                break

        return (result, input)

    return f


def parse_step(input: str) -> Result[Optional[Step]]:
    input = input.lstrip()
    (line, _, rest) = input.partition("\n")
    (head, _, name) = line.partition(" ")
    type = StepType.from_type(head)
    if type is not None:
        return (Step(type, name), rest)

    return (None, input)


parse_steps = create_parse_multiple(parse_step)


def parse_scenario(
    input: str, expect_head: str = "scenario"
) -> Result[Optional[Scenario]]:
    orig_input = input
    input = input.lstrip()
    (decl, _, input) = input.partition("\n")
    (head, _, name) = decl.partition(":")
    head = head.strip().lower()
    name = name.lstrip()
    if head != expect_head:
        return (None, orig_input)

    (steps, input) = parse_steps(input)
    return (Scenario(name, steps), input)


parse_scenarios = create_parse_multiple(parse_scenario)

