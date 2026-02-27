
# IoTFlow DSL

IoTFlow DSL is a domain-specific language for modeling, validating, and generating configurations for Internet of Things (IoT) systems.  
The language provides a structured and technology-agnostic way to describe IoT devices, their properties, and rule-based behavior.

This project was developed as part of an academic course focused on **Domain-Specific Languages (DSLs)** and language engineering using the **textX** framework.

---

## Motivation

Modeling IoT systems often involves combining sensors, actuators, and conditional logic. Using general-purpose programming languages for configuration can lead to verbose and error-prone setups.

IoTFlow DSL aims to:

- Simplify IoT system specification
- Provide early semantic validation of modeling errors
- Enable automated configuration generation
- Offer CLI integration through textX
- Support editor tooling via Language Server Protocol (LSP)

---

## Features

- DSL for defining IoT devices (sensors and actuators)
- Rule-based behavior definition using `when-then` constructs
- Semantic validation of models
- JSON configuration generation
- textX CLI integration
- Installable Python package
- Ready for editor support (textX-LS)

---

## Example Model

```dsl
sensor TemperatureSensor {
    type: DHT22
    unit: celsius
}

actuator Fan {
    type: relay
}

rule HighTemperatureRule {
    when TemperatureSensor.value > 30
    then Fan.turn_on
}
```

---

## Installation

### Prerequisites

- Python 3.9+
- Virtual environment tool (recommended)

### Install from Source

```bash
git clone https://github.com/0101dusica/iotflow-dsl.git
cd iotflow-dsl

python -m venv venv
source venv/bin/activate

pip install -e .
pip install textX[cli]
```

---

## Verify Installation

Check that the language and generator are registered:

```bash
textx list-languages
textx list-generators
```

You should see:

- `iotflow` language
- `json` generator for iotflow

---

## Usage

### IoTFlow CLI

IoTFlow provides its own CLI commands for model validation and parsing:

#### Validate a Model

```bash
python -m iotflow.cli validate examples/basic.iot
```

#### Parse and Display Model Info

```bash
python -m iotflow.cli parse examples/basic.iot
```

### textX CLI (Alternative)

You can also use standard textX commands:

#### Validate a Model

```bash
textx check examples/basic.iot
```

#### Generate JSON Configuration

```bash
textx generate examples/basic.iot --target json
```

This will generate a JSON file in the same directory as the model file.

---

## Examples

The `examples/` directory contains comprehensive IoTFlow DSL demonstrations:

- **`basic.iot`** - Simple temperature sensor and fan control
- **`multi_sensor.iot`** - Multiple sensors with coordinated rules  
- **`complex_rules.iot`** - All comparison operators (`<=`, `>=`, `<`, `!=`, `>`, `==`)
- **`home_automation.iot`** - Realistic home automation scenario
- **`smart_greenhouse.iot`** - Complex agricultural IoT system
- **`edge_cases.iot`** - Grammar boundary testing and naming conventions
- **`validation_test.iot`** - Error testing for LSP validation

Each example demonstrates different aspects of the DSL and validates successfully.

### Python API

Generate JSON directly in Python:

```python
from iotflow.generators.json_generator import model_to_json_string
from iotflow.language import iotflow_language
from textx import metamodel_from_file

# Load model and generate JSON
mm = metamodel_from_file('iotflow/grammar/iotflow.tx')
model = mm.model_from_file('examples/basic.iot')
json_output = model_to_json_string(model)
print(json_output)
```

### Direct JSON Generation

You can also generate JSON using the built-in generator:

```python
from iotflow.generators.json_generator import generate_json

# Generate JSON file directly
generate_json(model, 'output.json')
```

---

## Example Generated Output

```json
{
    "sensors": [
        {
            "name": "TemperatureSensor",
            "type": "DHT22",
            "unit": "celsius"
        }
    ],
    "actuators": [
        {
            "name": "Fan",
            "type": "relay"
        }
    ],
    "rules": [
        {
            "name": "HighTemperatureRule",
            "condition": {
                "sensor": "TemperatureSensor",
                "attribute": "value",
                "operator": ">",
                "value": 30
            },
            "action": {
                "actuator": "Fan",
                "command": "turn_on"
            }
        }
    ]
}
```

---

## Build Wheel Package (Optional)

To build a distributable wheel:

```bash
pip install build
python -m build
```

Install from the generated wheel:

```bash
pip install dist/iotflow_dsl-0.1.0-py3-none-any.whl
```

---

## Project Structure

```
iotflow-dsl/
├── iotflow/
│   ├── grammar/
│   ├── validators/
│   ├── generators/
│   ├── language.py
│   └── ...
├── examples/
├── pyproject.toml
└── README.md
```

---

## Development and Project Management

- Open-source project hosted on GitHub
- Tasks tracked using GitHub Issues
- Progress managed via Kanban board
- All evaluated work available on the `main` branch
- Commits linked to corresponding issues

---

## Editor Support

IoTFlow DSL is designed for Language Server Protocol (LSP) integration:

- Ready for textX-LS support  
- Syntax highlighting and validation in VS Code
- Real-time error detection
- IntelliSense capabilities

See [Editor Setup Instructions](docs/editor-setup.md) for detailed configuration.

---

## Validation Features

The DSL includes comprehensive semantic validation:

- **Device Reference Validation**: Ensures sensors and actuators exist before being referenced
- **Rule Validation**: Validates actuator actions against allowed command list
- **Grammar Validation**: Enforces proper syntax and structure
- **Type Safety**: Consistent property definitions across devices

Errors are reported with clear messages and location information.

---

## Troubleshooting

**Grammar doesn't support comments**: If you get parse errors with `//` comments, remove them from `.iot` files. The current grammar doesn't include comment support.

**Module not found**: Ensure the package is installed with `pip install -e .` and that your virtual environment is activated.

**textX commands not working**: Install textX CLI tools with `pip install textX[cli]` and verify language registration with `textx list-languages`.

---

## License

This project is licensed under an OSI-approved open-source license.  
See the LICENSE file for details.

---

## Author

R2 26/2025 Dušica Trbović  
Master Studies - Software Engineering
