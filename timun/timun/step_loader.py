from typing import DefaultDict, List, Dict
import importlib, importlib.util
import os
from os.path import basename, join, isfile, abspath
import itertools
import sys
from collections import defaultdict

from timun.step import StepDescriptor, StepDict


class DuplicateStepException(Exception):
    def __init__(self, step1: StepDescriptor, step2: StepDescriptor):
        self.message = f"Duplicate step {step1.summary()} and {step2.summary()}"
        super().__init__(self.message)


def all_py_files_in_dir(dir: str):
    return [
        join(dir, f)
        for f in os.listdir(dir)
        if isfile(join(dir, f)) and f.endswith(".py")
    ]


def load_file(filename: str):
    # filename = abspath(filename)
    file_path = filename
    module_name = basename(file_path)[:-3]

    if not isfile(file_path):
        raise Exception(f"invalid import path f{file_path}")

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)  # type: ignore
    return module


def load_step_from_file(filename: str):
    module = load_file(filename)

    defined_steps = []

    for x in module.__dict__:
        obj = getattr(module, x)

        step_desc: StepDescriptor = getattr(obj, "__TIMUN_STEP__", None)
        if step_desc:
            step_desc.filename = filename
            defined_steps.append(step_desc)

    return defined_steps


def load_steps_from_dir(dir: str):
    files = all_py_files_in_dir(dir)
    steps = itertools.chain(*map(load_step_from_file, files))

    return list(steps)


def load_environment(dir: str):
    p = join(dir, "environment.py")
    try:
        return load_file(p)
    except:
        return None


def steps_to_dict(steps: List[StepDescriptor]):
    result: StepDict = {}

    for step in steps:
        key = f"{step.type.name} {step.text}"
        if key in result:
            raise DuplicateStepException(step, result[step.text])

        result[key] = step

    return result
