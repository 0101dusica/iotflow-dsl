from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TxNode:
    parent: Optional[object] = field(default=None, repr=False)
