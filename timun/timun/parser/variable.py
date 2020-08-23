from timun.model import Variable, VariableDeclaration
from typing import List, Tuple
from timun.parser.combinator import (
    ParserError,
    ParserInput,
    ParserResult,
    next_nonempty_line,
    one_or_more,
)
from .decorator import parser


@parser("variable line")
def parse_variable_line(input: ParserInput) -> ParserResult[Variable]:
    cur_line, cur_idx, next_input = next_nonempty_line(input)

    name, comma, tail = cur_line.partition(":")

    type, value = parse_variable_type(tail, input)

    return Variable(name, type, value, cur_idx), next_input


def parse_variable_type(line: str, input: ParserInput):
    head, _, tail = line.strip().partition(" ")
    head = head.lower()

    if head == "enum":
        val = [x.strip() for x in tail.split(",")]
        return head, val

    if head == "bool":
        val = ["true", "false"]
        return head, val

    raise ParserError(f"Unexpected variable type '{head}'", input)


@parser("variable declaration")
def parse_variable(input: ParserInput):
    cur_line, cur_idx, next_input = next_nonempty_line(input)
    head, _, _ = cur_line.partition(":")
    head = head.strip().lower()

    if head != "variable":
        raise ParserError(f"Expected 'variable', found '{head}'", input)

    variables, next_input = one_or_more(parse_variable_line)(next_input)

    return VariableDeclaration(variables, cur_idx, input.filename), next_input
