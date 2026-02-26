
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

### Validate a Model

```bash
textx check examples/basic.iot
```

### Generate JSON Configuration

```bash
textx generate examples/basic.iot --target json
```

This will generate a JSON file in the same directory as the model file.

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

See [Editor Setup Instructions](docs/editor-setup.md)

---

## License

This project is licensed under an OSI-approved open-source license.  
See the LICENSE file for details.

---

## Author

R2 26/2025 Dušica Trbović  
Master Studies - Software Engineering
