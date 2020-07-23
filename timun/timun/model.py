from typing import Optional, List
from dataclasses import dataclass
from enum import Enum


class StepType(Enum):
    GIVEN = 0
    WHEN = 1
    THEN = 2

    @classmethod
    def from_string(cls, input: str) -> Optional["StepType"]:
        input = input.strip().upper()
        return getattr(StepType, input, None)


@dataclass
class Step:
    type: StepType
    text: str
    idx: int


class ScenarioType(Enum):
    SCENARIO = 0
    BACKGROUND = 1
    FAIL_SCENARIO = 2

    @classmethod
    def from_string(cls, input: str) -> Optional["ScenarioType"]:
        input = input.strip().upper()
        if input == "FAIL SCENARIO":
            return cls.FAIL_SCENARIO

        return getattr(ScenarioType, input, None)


@dataclass
class Scenario:
    keyword: ScenarioType
    text: str
    steps: List[Step]
    idx: int


@dataclass
class Feature:
    tags: List[str]
    text: str
    background: Optional[Scenario]
    scenarios: List[Scenario]
    idx: int
    filename: str

