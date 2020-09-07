from typing import Dict, Iterator, Literal, Optional, List, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum

TableEntry = List[str]
TableType = Literal["example", "fail example", "variable accepted", "variable rejected"]
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

    def pretty(self) -> str:
        return f"{self.type.name}\t{self.text}"


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

    def invert(self) -> "ScenarioType":
        if self == ScenarioType.SCENARIO:
            return ScenarioType.FAIL_SCENARIO
        elif self == ScenarioType.FAIL_SCENARIO:
            return ScenarioType.SCENARIO
        return ScenarioType.BACKGROUND


@dataclass
class Scenario:
    type: ScenarioType
    text: str
    steps: List[Step]

    idx: int

    variable_accepted: Optional[Table]
    variable_rejected: Optional[Table]


@dataclass
class ScenarioOutline:
    text: str
    steps: List[Step]

    example_table: Optional[Table]
    fail_example_table: Optional[Table]

    idx: int

    variable_accepted: Optional[Table] = None
    variable_rejected: Optional[Table] = None


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

    var_dict: Dict[str, Variable] = field(init=False)

    def __post_init__(self):
        self.var_dict = {}

        for var in self.variables:
            self.var_dict[var.name] = var
