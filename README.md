# IoTFlow DSL

IoTFlow DSL is a domain-specific language for modeling, validating, and generating configurations for Internet of Things (IoT) systems.  
The language is designed to provide a clear and structured way to describe IoT devices, their properties, and rule-based behavior in a technology-agnostic manner.

This project is developed as part of an academic course focused on domain-specific languages, language engineering, and tooling support using the **textX** framework.

---

## Motivation

Modeling IoT systems often involves combining multiple concepts such as sensors, actuators, and conditional logic. Using a general-purpose language for this task can lead to verbose and error-prone configurations.

IoTFlow DSL aims to:
- simplify IoT system specification,
- provide early validation of common modeling errors,
- enable automated generation of configuration artifacts,
- offer editor support through the Language Server Protocol (LSP).

---

## Features

- DSL for defining IoT devices (sensors and actuators)
- Rule-based behavior definition using `when–then` constructs
- Semantic validation of models
- Code and configuration generation
- Editor support (syntax highlighting and code completion)
- Installable Python package

---

## Example

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

## Architecture Overview

The project consists of the following main components:

- **Grammar definition** – implemented using textX
- **Semantic validation layer** – ensures model correctness
- **Generators** – produce configuration artifacts from models
- **Language Server** – enables editor features such as completion and highlighting
- **CLI integration** – allows model processing via command line

---

## Installation

### Prerequisites

- Python 3.9+
- Virtual environment tool (recommended)

### Install from source

```bash
git clone https://github.com/0101dusica/iotflow-dsl.git
cd iotflow-dsl
python -m venv venv
source venv/bin/activate
pip install -e .
```

---

## Usage

### Parsing a model

```bash
textx check examples/example.iot
```

### Generating artifacts

```bash
textx generate examples/example.iot
```

Generated files will be placed in the configured output directory.

---

## Editor Support

IoTFlow DSL provides editor support via the **Language Server Protocol** using `textX-LS`.

Supported features:
- Syntax highlighting
- Code completion
- Basic diagnostics

The language server can be used with editors such as **VS Code**.

---

## Project Structure

```text
iotflow-dsl/
├── iotflow/
│   ├── grammar/
│   ├── validators/
│   ├── generators/
│   └── cli.py
├── examples/
├── pyproject.toml
└── README.md
```

---

## Development and Project Management

- The project is hosted on GitHub as an open-source repository
- Tasks are tracked using GitHub Issues
- Project progress is managed using a Kanban board
- All evaluated work is available on the `main` branch
- Commits are linked to corresponding issues

---

## License

This project is licensed under an OSI-approved open-source license.  
The specific license is defined in the repository.

---

## Author

R2 26/2025 Dušica Trbović
