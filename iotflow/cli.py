import argparse
from pathlib import Path

from .parser.parse import parse_file
from .model import Sensor, Actuator, Rule
from .runtime.runner import run_simulation


def validate_model(model_file):
    """Validate an IoTFlow model file."""
    try:
        model = parse_file(Path(model_file))

        sensors = [el for el in model.elements if isinstance(el, Sensor)]
        actuators = [el for el in model.elements if isinstance(el, Actuator)]
        rules = [el for el in model.elements if isinstance(el, Rule)]

        print(f"✓ Model parsed successfully: {model_file}")
        print(f"  - Sensors: {len(sensors)}")
        print(f"  - Actuators: {len(actuators)}")
        print(f"  - Rules: {len(rules)}")

        return True

    except Exception as e:
        print(f"✗ Error parsing model {model_file}: {e}")
        return False


def parse_command(args):
    """Parse a model file and show basic info."""
    try:
        model = parse_file(Path(args.model))
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


def run_command(args):
    """Run IoT simulation on a model file."""
    try:
        model = parse_file(Path(args.model))
        result = run_simulation(model, cycles=args.cycles)
        print(result)
        return True
    except Exception as e:
        print(f"Error running simulation: {e}")
        return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="IoTFlow DSL CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    validate_parser = subparsers.add_parser('validate', help='Validate an IoTFlow model')
    validate_parser.add_argument('model', help='Path to the model file to validate')

    parse_parser = subparsers.add_parser('parse', help='Parse and display IoTFlow model info')
    parse_parser.add_argument('model', help='Path to the model file to parse')

    run_parser = subparsers.add_parser('run', help='Run IoT simulation')
    run_parser.add_argument('model', help='Path to the model file to simulate')
    run_parser.add_argument('--cycles', type=int, default=1, help='Number of simulation cycles')

    args = parser.parse_args()

    if args.command == 'validate':
        success = validate_model(args.model)
        exit(0 if success else 1)
    elif args.command == 'parse':
        success = parse_command(args)
        exit(0 if success else 1)
    elif args.command == 'run':
        success = run_command(args)
        exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
