from typing import Callable, List, NamedTuple, Tuple, TypeVar, Optional


class ParserInput(NamedTuple):
    lines: List[str]
    idx: int
    filename: str


T = TypeVar("T")
ParserResult = Tuple[T, ParserInput]
Parser = Callable[[ParserInput], ParserResult[T]]


class ParserError(Exception):
    def __init__(
        self, message: str, input: ParserInput, parent: Optional["ParserError"] = None
    ):
        self.parent = parent

        # if self.parent:
        #     self.message: str = self.parent.message + "\n"
        # else:
        self.message = ""

        self.message += f"{message} [{input.filename}:{input.idx+1}]"
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


def ignore_line(input: ParserInput) -> ParserInput:
    while True:
        line, idx, next_input = next_line(input)
        line = line.strip()
        if line != "" and line[0] != "#":
            return input
        input = next_input


def next_nonempty_line(input: ParserInput) -> Tuple[str, int, ParserInput]:
    while True:
        line, idx, next_input = next_line(input)
        line = line.strip()
        if line != "" and line[0] != "#":
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
        exception = None
        try:
            res, next_input = zero_or_more(parser)(input)
            if res != []:
                return res, next_input
        except ParserError as p:
            exception = p
        raise ParserError(f"expected one or more '{parser.__PARSER__}'", input, exception)  # type: ignore

    return f


def parser_or(*parsers: Parser) -> Parser:
    desc_line = " or ".join([p.__PARSER__ for p in parsers])  # type: ignore

    def f(input: ParserInput) -> ParserResult:
        exception = None
        for parser in parsers:
            try:
                result = parser(input)
                return result
            except ParserError as p:
                exception = p
                continue

        raise ParserError(f"expected one of {desc_line}", input, exception)

    setattr(f, "__PARSER__", desc_line)

    return f
