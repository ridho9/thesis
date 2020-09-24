import sys
import os
from os.path import join

from pprint import pprint
from typing import List
from timun.model import Feature, Scenario, VariableDeclaration
from timun.file_loader import parse_features_dir
from timun.scrambler import RandomScrambleStrategy, Scrambler
from timun.step_loader import load_environment, load_steps_from_dir, steps_to_dict
from timun.runner import TestRunner
import timun.expander as expander

import click


@click.command()
@click.option("--scramble/--noscramble", "-S/-NS", default=True)
@click.option("--seed", default="asdas")
def main(scramble: bool, seed: str):
    print("Starting timun")
    # Load Features

    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.append(cwd)

    folder = "features"
    items = parse_features_dir(folder)
    # pprint(features, indent=2)

    features: List[Feature] = list(filter(lambda f: isinstance(f, Feature), items))  # type: ignore

    #  Expand features
    expanded_features = list(map(expander.expand_feature, features))

    variables: List[VariableDeclaration] = list(
        filter(lambda f: isinstance(f, VariableDeclaration), items)  # type: ignore
    )

    # TODO: merge variables declaration
    if variables and len(variables) != 0:
        variable = variables[0]

        # Expand variables
        expanded_variables = list(
            map(
                lambda feature: expander.expand_variables_feature(variable, feature),
                expanded_features,
            )
        )
    else:
        expanded_variables = expanded_features

    # Load Step Descriptor
    step_folder = join(folder, "steps")
    steps = load_steps_from_dir(step_folder)
    step_dict = steps_to_dict(steps)
    # pprint(step_dict)

    # Run Test
    environment = load_environment(folder)

    runner = TestRunner(expanded_variables, step_dict, environment)
    runner.run()

    print("==========================")

    if scramble:
        scrambler = Scrambler(
            expanded_variables, step_dict, environment, seed=seed, amount=50
        )
        scrambler.run()
