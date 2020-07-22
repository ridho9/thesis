from os.path import join

from pprint import pprint
from timun.file_loader import parse_features_dir
from timun.step_loader import load_steps_from_dir, steps_to_dict
from timun.runner import TestRunner


def main():
    folder = "features"
    features = parse_features_dir(folder)
    # pprint(features)

    step_folder = join(folder, "steps")
    steps = load_steps_from_dir(step_folder)
    step_dict = steps_to_dict(steps)
    # pprint(step_dict)

    runner = TestRunner(features, step_dict)
    runner.run()
