from typing import List
from .combinator import ParserError, ParserInput, ParserResult, next_nonempty_line

TableLine = List[str]
Table = List[TableLine]


def parse_table_line(input: ParserInput) -> ParserResult[TableLine]:
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


setattr(parse_table_line, "__PARSER__", "table-line")


def parse_table(input: ParserInput) -> ParserResult[Table]:
    result: Table = []

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


setattr(parse_table, "__PARSER__", "table")
