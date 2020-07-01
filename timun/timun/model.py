from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class StepType(Enum):
    GIVEN = 1
    WHEN = 2
    THEN = 3

    @classmethod
    def from_type(cls, head: str) -> Optional["StepType"]:
        head = head.upper()
        return getattr(cls, head, None)


@dataclass
class Step:
    type: StepType
    name: str


@dataclass
class Scenario:
    name: str
    steps: List[Step]


@dataclass
class Feature:
    name: str
    scenarios: List[Scenario]

    desc: Optional[str] = None
    background: Optional[Scenario] = None
