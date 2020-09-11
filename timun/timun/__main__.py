import sys
import os
from os.path import join

from pprint import pprint
from timun.model import Feature, Scenario, VariableDeclaration
from timun.file_loader import parse_features_dir
from timun.scrambler import RandomScrambleStrategy, Scrambler
from timun.step_loader import load_environment, load_steps_from_dir, steps_to_dict
from timun.runner import TestRunner
import timun.expander as expander


def main():
    print("Starting timun")
    # Load Features

    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.append(cwd)

    folder = "features"
    items = parse_features_dir(folder)
    # pprint(features, indent=2)

    features = list(filter(lambda f: isinstance(f, Feature), items))

    #  Expand features
    expanded_features = list(map(expander.expand_feature, features))

    variables = list(filter(lambda f: isinstance(f, VariableDeclaration), items))

    # TODO: merge variables declaration
    if variables and len(variables) != 0:
        variables = variables[0]

    # Expand variables
    expanded_variables = list(
        map(
            lambda feature: expander.expand_variables_feature(variables, feature),
            expanded_features,
        )
    )

    # Load Step Descriptor
    step_folder = join(folder, "steps")
    steps = load_steps_from_dir(step_folder)
    step_dict = steps_to_dict(steps)
    # pprint(step_dict)

    # Run Test
    environment = load_environment(folder)

    runner = TestRunner(expanded_variables, step_dict, environment)
    runner.run()

    print("=========================")

    scrambler = Scrambler(
        expanded_variables, step_dict, environment, seed=".", amount=50
    )
    scrambler.run()
