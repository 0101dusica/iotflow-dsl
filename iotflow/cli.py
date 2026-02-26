# Entry point for IoTFlow DSL CLI.

import argparse
from . import load_model


def validate_model(model_file):
    """Validate an IoTFlow model file using the load_model function."""
    try:
        model = load_model(model_file)
        
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


def parse_command(args):
    """Parse a model file and show basic info (bonus command)."""
    try:
        model = load_model(args.model)
        print(f"Model loaded successfully from: {args.model}")
        print(f"Total elements: {len(model.elements)}")
        
        for i, element in enumerate(model.elements, 1):
            element_type = element.__class__.__name__
            element_name = element.name
            print(f"  {i}. {element_type}: {element_name}")
            
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="IoTFlow DSL CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate command  
    validate_parser = subparsers.add_parser('validate', help='Validate an IoTFlow model')
    validate_parser.add_argument('model', help='Path to the model file to validate')
    
    # Parse command (bonus)
    parse_parser = subparsers.add_parser('parse', help='Parse and display IoTFlow model info')
    parse_parser.add_argument('model', help='Path to the model file to parse')
    
    args = parser.parse_args()
    
    if args.command == 'validate':
        success = validate_model(args.model)
        exit(0 if success else 1)
    elif args.command == 'parse':
        success = parse_command(args)
        exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
