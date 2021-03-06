from typing import Callable, Dict, List
from dataclasses import dataclass

from timun.model import StepType

from parse import Parser
from parse import compile as pcompile


@dataclass
class StepDescriptor:
    type: StepType
    text: str
    pattern: Parser
    fields: List[str]
    filename: str
    function: Callable

    def summary(self):
        return f"['{self.text}':{self.function.__name__}:{self.filename}]"


StepDict = Dict[str, StepDescriptor]


def step(head, text: str):
    def decorator(func):
        # return func
        type = StepType.from_string(head)
        if type == None:
            raise Exception(f"invalid step type '{head}'")

        t = text.strip()
        pattern = pcompile(t)
        named_fields = pattern._named_fields
        descriptor = StepDescriptor(type, t, pattern, named_fields, "??", func)
        setattr(func, "__TIMUN_STEP__", descriptor)

        return func

    return decorator


given = lambda func: step("given", func)
when = lambda func: step("when", func)
then = lambda func: step("then", func)
