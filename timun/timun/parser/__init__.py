from .step import parse_step, parse_steps
from .combinator import create_input, ParserError, Parser
from .scenario import (
    parse_scenario_like,
    parse_fail_scenario,
    parse_scenario_family,
    parse_scenarios,
)
from .feature import parse_feature
from .table import parse_table_line, parse_table


def parser(name: str):
    def decorator(func: Parser):
        setattr(func, "__PARSER__", name)
        return func

    return decorator
