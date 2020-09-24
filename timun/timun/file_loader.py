import itertools
from timun.parser.combinator import ParserError, ignore_line, next_nonempty_line
from typing import List, Union
import os
from os.path import isfile, join, abspath

from timun.model import Feature, VariableDeclaration
import timun.parser as parser

from timun.step_loader import load_step_from_file


def all_feature_files_in_dir(dir: str) -> List[str]:
    return [
        join(dir, f)
        for f in os.listdir(dir)
        if isfile(join(dir, f)) and f.endswith(".feature")
    ]


def parse_feature_file(path: str) -> List[Union[Feature, VariableDeclaration]]:
    with open(path) as f:
        input = parser.create_input(path, f.read())

        features, input = parser.parse_top_level(input)

        for line in input.lines:
            line = line.strip()
            if line != "" and line[0] != "#":
                input = ignore_line(input)
                raise ParserError(
                    f"Failed to parse file '{path}', unexpected input '{line}'", input
                )

        return features


def parse_features_dir(dir: str) -> List[Union[Feature, VariableDeclaration]]:
    try:
        files = all_feature_files_in_dir(dir)
        features = itertools.chain(*map(parse_feature_file, files))

        return list(features)
    except ParserError as e:
        print(e.message)
        exit(1)
