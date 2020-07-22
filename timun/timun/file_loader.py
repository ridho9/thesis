import itertools
from typing import List
import os
from os.path import isfile, join, abspath

from timun.model import Feature
import timun.parser as parser

from timun.step_loader import load_step_from_file


def all_feature_files_in_dir(dir: str) -> List[str]:
    return [
        join(dir, f)
        for f in os.listdir(dir)
        if isfile(join(dir, f)) and f.endswith(".feature")
    ]


def parse_feature_file(path: str) -> List[Feature]:
    with open(path) as f:
        input = parser.create_input(path, f.read())

        features, input = parser.parse_features(input)

        return features


def parse_features_dir(dir: str) -> List[Feature]:
    files = all_feature_files_in_dir(dir)
    features = itertools.chain(*map(parse_feature_file, files))

    return list(features)
