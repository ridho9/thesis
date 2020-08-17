from typing import List, Tuple
from .combinator import (
    ParserError,
    ParserInput,
    ParserResult,
    next_nonempty_line,
    Parser,
    one_or_more,
    parser_or,
)
from .decorator import parser
from timun.model import Table, TableEntry


@parser("table line")
def parse_table_line(input: ParserInput) -> ParserResult[TableEntry]:
    cur_line, cur_idx, next_input = next_nonempty_line(input)
    cur_line = cur_line.strip()

    if not cur_line.startswith("|"):
        raise ParserError("Table line must starts with |", input)
    if not cur_line.endswith("|"):
        raise ParserError("Table line must ends with |", input)

    items = [x.strip() for x in cur_line.split("|")[1:-1]]

    if items == []:
        raise ParserError("Table can't be empty ('|')", input)

    for item in items:
        if item == "":
            raise ParserError("Table can't have empty entry", input)

    return items, next_input


@parser("table")
def parse_table_entries(input: ParserInput) -> ParserResult[List[TableEntry]]:
    result = []

    head, input = parse_table_line(input)
    head_len = len(head)
    result.append(head)

    while True:
        try:
            line, next_input = parse_table_line(input)

            if head_len != len(line):
                raise ParserError(
                    f"Different table head(f{head_len}) and entry(f{len(line)}) length",
                    input,
                )

            result.append(line)
            input = next_input
        except:
            break

    return result, input


@parser("named table")
def parse_named_table(name: str, input: ParserInput) -> ParserResult[Table]:
    cur_line, cur_idx, next_input = next_nonempty_line(input)
    head, _, rest = cur_line.partition(":")
    head = head.strip().lower()

    if head != name:
        raise ParserError(f"Found '{head}' expect '{name}'", input)

    table, next_input = parse_table_entries(next_input)
    return (head, table), next_input


parse_table_example = parser("example")(
    lambda input: parse_named_table("example", input)
)

parse_table_outline = parser("table outline")(parser_or(parse_table_example))

parse_tables_outline = parser("tables outline")(one_or_more(parse_table_outline))
