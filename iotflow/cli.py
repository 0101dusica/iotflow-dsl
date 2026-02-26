# Entry point for IoTFlow DSL CLI.

import os
import argparse
from pathlib import Path
from textx import metamodel_from_file


def get_grammar_path():
    """Get path to the IoTFlow grammar file."""
    this_dir = Path(__file__).parent
    return this_dir / "grammar" / "iotflow.tx"


def parse_model(model_file):
    """Parse an IoTFlow model file and return the parsed model."""
    grammar_path = get_grammar_path()
    
    if not grammar_path.exists():
        raise FileNotFoundError(f"Grammar file not found at: {grammar_path}")
    
    if not Path(model_file).exists():
        raise FileNotFoundError(f"Model file not found at: {model_file}")
    
    # Create metamodel from grammar
    metamodel = metamodel_from_file(str(grammar_path))
    
    # Parse the model
    model = metamodel.model_from_file(model_file)
    
    return model


def validate_model(model_file):
    """Validate an IoTFlow model file."""
    try:
        model = parse_model(model_file)
        
        # Count elements
        sensors = [el for el in model.elements if el.__class__.__name__ == 'Sensor']
        actuators = [el for el in model.elements if el.__class__.__name__ == 'Actuator']
        rules = [el for el in model.elements if el.__class__.__name__ == 'Rule']
        
        print(f"✓ Model parsed successfully: {model_file}")
        print(f"  - Sensors: {len(sensors)}")
        print(f"  - Actuators: {len(actuators)}")
        print(f"  - Rules: {len(rules)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error parsing model {model_file}: {e}")
        return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="IoTFlow DSL CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate an IoTFlow model')
    validate_parser.add_argument('model', help='Path to the model file to validate')
    
    args = parser.parse_args()
    
    if args.command == 'validate':
        success = validate_model(args.model)
        exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
