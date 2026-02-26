# This file marks the iotflow package for IoTFlow DSL.

from pathlib import Path
from textx import metamodel_from_file


def load_model(model_path: str):
    """
    Load and parse an IoTFlow model file.
    
    Args:
        model_path (str): Path to the .iot model file to parse
        
    Returns:
        textX model object containing the parsed IoT model
        
    Raises:
        FileNotFoundError: If the grammar or model file is not found
        textx.exceptions.TextXSyntaxError: If the model has syntax errors
    """
    # Get path to grammar file relative to this package
    this_dir = Path(__file__).parent
    grammar_path = this_dir / "grammar" / "iotflow.tx"
    
    if not grammar_path.exists():
        raise FileNotFoundError(f"Grammar file not found at: {grammar_path}")
    
    if not Path(model_path).exists():
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    
    # Create metamodel from grammar
    metamodel = metamodel_from_file(str(grammar_path))
    
    # Parse and return the model
    model = metamodel.model_from_file(model_path)
    return model


# Package metadata
__version__ = "0.1.0"
__all__ = ["load_model"]
