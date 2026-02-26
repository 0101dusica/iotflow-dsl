"""
textX CLI generator for IoTFlow DSL to JSON conversion.

This module provides a textX generator that can be invoked using:
    textx generate model.iot --target json
"""

from textx import generator
from pathlib import Path
from .json_generator import generate_json


@generator('iotflow', 'json')
def json_generator_cli(metamodel, model, output_path, overwrite, debug):
    """
    textX CLI generator for converting IoTFlow models to JSON.
    
    Args:
        metamodel: The metamodel used to parse the model
        model: The parsed IoTFlow model object
        output_path: Path where generated files should be placed
        overwrite: Whether to overwrite existing files
        debug: Debug mode flag
    """
    # Create output file path
    output_path = Path(output_path)
    
    # Use model filename as base for JSON output
    if hasattr(model, '_tx_model_file') and model._tx_model_file:
        model_file = Path(model._tx_model_file)
    elif hasattr(model, '_tx_filename') and model._tx_filename:
        model_file = Path(model._tx_filename)
    else:
        # Fallback to generic name
        model_file = Path("model.iot")
    
    # Create JSON filename
    json_filename = model_file.stem + ".json"
    output_file = output_path / json_filename
    
    # Check overwrite protection
    if output_file.exists() and not overwrite:
        raise Exception(f"Output file {output_file} already exists. Use --overwrite to replace it.")
    
    # Generate JSON
    if debug:
        print(f"Generating JSON for IoTFlow model...")
        print(f"Input model: {model_file}")
        print(f"Output file: {output_file}")
    
    generate_json(model, str(output_file))
    
    if debug:
        print(f"JSON generated successfully: {output_file}")