from typing import Literal, Optional, List, Tuple, Union
from dataclasses import dataclass
from enum import Enum

TableEntry = List[str]
TableType = Literal["example", "fail example"]
Table = Tuple[TableType, List[TableEntry]]


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
class ScenarioOutline:
    text: str
    steps: List[Step]

    example_table: Optional[Table]
    fail_example_table: Optional[Table]

    idx: int


@dataclass
class Feature:
    tags: List[str]
    text: str
    background: Optional[Scenario]
    scenarios: List[Union[Scenario, ScenarioOutline]]
    idx: int
    filename: str


VariableType = Union[Literal["enum"], Literal["bool"]]


@dataclass
class Variable:
    name: str
    type: VariableType
    values: List[str]
    idx: int


@dataclass
class VariableDeclaration:
    variables: List[Variable]
    idx: int
    filename: str
