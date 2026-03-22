from dataclasses import dataclass, field

from iotflow.model.base import TxNode


@dataclass
class TypeProperty(TxNode):
    value: str = ""


@dataclass
class UnitProperty(TxNode):
    value: str = ""


@dataclass
class Sensor(TxNode):
    name: str = ""
    properties: list = field(default_factory=list)


@dataclass
class Actuator(TxNode):
    name: str = ""
    properties: list = field(default_factory=list)
