from .combinator import Parser, ParserError, create_input, one_or_more, parser_or
from .feature import parse_feature, parse_features
from .scenario import (
    parse_fail_scenario,
    parse_scenario_family,
    parse_scenario_like,
    parse_scenarios,
    parse_scenario_outline,
)
from .step import parse_step, parse_steps
from .table import parse_table_line, parse_table_entries, parse_named_table
from .variable import parse_variable_line, parse_variable

parse_top_level_item = parser_or(parse_variable, parse_feature)
parse_top_level = one_or_more(parse_top_level_item)
