from dataclasses import dataclass, field

from iotflow.model.base import TxNode


@dataclass
class Model(TxNode):
    elements: list = field(default_factory=list)
