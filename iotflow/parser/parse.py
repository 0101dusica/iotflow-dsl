from pathlib import Path

from .metamodel import build_metamodel
from ..model import Model


def parse_file(path: Path) -> Model:
    """
    Parses DSL file and returns typed Model.
    """
    mm = build_metamodel()
    model: Model = mm.model_from_file(str(path))
    return model


def parse_str(text: str) -> Model:
    """
    Parses DSL string (used mainly in tests).
    """
    mm = build_metamodel()
    model: Model = mm.model_from_str(text)
    return model
