from pathlib import Path

from .parser.parse import parse_file, parse_str
from .model import Model


def load_model(model_path: str) -> Model:
    """
    Load and parse an IoTFlow model file with semantic validation.
    """
    return parse_file(Path(model_path))


__version__ = "0.1.0"
__all__ = ["load_model", "parse_file", "parse_str", "Model"]
