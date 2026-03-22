from dataclasses import dataclass
from enum import Enum
from typing import Optional

from iotflow.model.base import TxNode


class ComparisonOp(Enum):
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="
    EQ = "=="
    NEQ = "!="


@dataclass
class SensorRef(TxNode):
    sensor_name: str = ""


@dataclass
class ActuatorRef(TxNode):
    actuator_name: str = ""


@dataclass
class Condition(TxNode):
    sensor_ref: Optional[SensorRef] = None
    operator: str = ""
    value: float = 0.0


@dataclass
class Action(TxNode):
    actuator_ref: Optional[ActuatorRef] = None
    action_name: str = ""


@dataclass
class WhenClause(TxNode):
    condition: Optional[Condition] = None


@dataclass
class ThenClause(TxNode):
    action: Optional[Action] = None


@dataclass
class Rule(TxNode):
    name: str = ""
    when_clause: Optional[WhenClause] = None
    then_clause: Optional[ThenClause] = None
