# IoTFlow DSL

IoTFlow DSL is a domain-specific language for **modeling, validating, simulating, and generating configurations** for Internet of Things (IoT) systems. It provides a structured, technology-agnostic, human-readable way to describe IoT devices, zones, properties, and rule-based behavior - and automatically generates deployable configuration artifacts from those models.

This project was developed as part of an academic course focused on **Domain-Specific Languages (DSLs)** and language engineering using the **textX** framework.

---

## Why IoTFlow?

Existing IoT configuration approaches all have significant limitations at scale:

| Tool | Limitation |
|---|---|
| **Node-RED** | Visual-only; flows can't be version-controlled, code-reviewed, or reused across systems |
| **Home Assistant YAML** | Platform-specific; becomes unreadable and error-prone on complex systems |
| **AWS IoT Things Graph** | Cloud-only; vendor lock-in, no offline validation |
| **Custom scripts** | No structure, no validation, no reuse - every system is rebuilt from scratch |

IoTFlow offers a **text-based, platform-agnostic DSL** that can be version-controlled, code-reviewed, and validated before deployment. Models are readable by both engineers and domain experts. The language enforces correctness at authoring time - not at runtime when failures are costly.

---

## Features

### Language (DSL)
- Define IoT **devices** (sensors and actuators) with typed properties
- Organize devices into **zones** representing physical spaces or subsystems
- **Rule-based behavior** using expressive `when-then` constructs:
  - Numeric comparisons (`>`, `<`, `>=`, `<=`, `==`, `!=`)
  - Multi-condition logic with `AND` / `OR`
  - Device state checks (`state == active`)
  - Time-based conditions (`time between 22:00 and 06:00`)
  - Threshold alerts with severity levels (`severity: critical`)
- **Delayed and sequential actions** (`after 10s`)
- **Priority levels** on rules to resolve conflicts

### Validation
- Undefined device references
- Invalid actuator commands per device type
- Rule conflicts and unreachable conditions
- Zone scoping violations
- Time range format errors
- Circular rule dependencies

### Generators
- **JSON** - for MQTT brokers and custom IoT runtimes
- **Home Assistant YAML** - ready-to-deploy automation configuration
- **Graphviz DOT** - visual topology diagram of zones, devices, and rule relationships

### Simulator
- Event-driven simulation of a model using mock sensor values
- Rule firing trace - shows which rules trigger and in what order
- Conflict detection at runtime - identifies rules with contradictory actions
- CLI command: `iotflow simulate examples/smart_city.iot --events examples/smart_city_events.json`

### Tooling
- textX CLI integration (`textx check`, `textx generate`)
- IoTFlow CLI (`iotflow validate`, `iotflow parse`, `iotflow simulate`)
- LSP support via textX-LS (syntax highlighting, real-time validation, IntelliSense in VS Code)
- Installable Python package

---

## Flagship Example - Smart City

The following model describes a segment of a smart city system with three operational zones: traffic management, environmental monitoring, and public infrastructure. This is the kind of real-world complexity IoTFlow is designed for.

```
zone TrafficDistrict {

  sensor TrafficDensitySensor {
    type: inductive_loop
    unit: vehicles_per_minute
  }

  sensor EmergencyVehicleSensor {
    type: acoustic
    unit: boolean
  }

  actuator TrafficLight {
    type: rgb_signal
  }

  actuator VariableSpeedSign {
    type: led_display
  }

  actuator EmergencyCorridorSystem {
    type: relay
  }

}

zone EnvironmentalZone {

  sensor AirQualitySensor {
    type: electrochemical
    unit: AQI
  }

  sensor CO2Sensor {
    type: NDIR
    unit: ppm
  }

  sensor NoiseSensor {
    type: microphone
    unit: dB
  }

  sensor FloodSensor {
    type: ultrasonic
    unit: cm
  }

  actuator PollutionAlarm {
    type: buzzer
    severity: critical
  }

  actuator EmergencyBroadcast {
    type: speaker
    severity: critical
  }

  actuator DrainageValve {
    type: servo
  }

}

zone PublicInfrastructure {

  sensor AmbientLightSensor {
    type: photodiode
    unit: lux
  }

  sensor PedestrianSensor {
    type: infrared
    unit: boolean
  }

  sensor TemperatureSensor {
    type: DS18B20
    unit: celsius
  }

  actuator StreetLighting {
    type: dimmable_led
  }

  actuator HeatingSystem {
    type: relay
  }

  actuator PublicDisplayBoard {
    type: led_matrix
  }

}

rule HeavyTrafficResponse {
  priority: high
  when TrafficDensitySensor.value > 60 AND EmergencyVehicleSensor.state == inactive
  then TrafficLight.set_mode slow, VariableSpeedSign.display "CONGESTION - 30km/h"
}

rule EmergencyCorridorActivation {
  priority: critical
  when EmergencyVehicleSensor.state == active
  then EmergencyCorridorSystem.activate, TrafficLight.set_mode emergency after 2s
}

rule AirPollutionAlert {
  priority: high
  when AirQualitySensor.value > 150 OR CO2Sensor.value > 1000
  then PollutionAlarm.trigger, PublicDisplayBoard.display "HIGH POLLUTION - LIMIT OUTDOOR ACTIVITY"
}

rule NightLighting {
  when time between 20:00 and 06:00 AND AmbientLightSensor.value < 50
  then StreetLighting.turn_on
}

rule PedestrianDimming {
  when time between 01:00 and 05:00 AND PedestrianSensor.state == inactive
  then StreetLighting.set_level 30
}

rule FloodEmergency {
  priority: critical
  when FloodSensor.value > 80
  then DrainageValve.open, EmergencyBroadcast.announce "FLOOD RISK - EVACUATE LOW AREAS" after 10s
}

rule WinterRoadHeating {
  when TemperatureSensor.value < 2 AND time between 04:00 and 08:00
  then HeatingSystem.turn_on
}

rule NoisePollutionWarning {
  when NoiseSensor.value > 85 AND time between 22:00 and 07:00
  then PublicDisplayBoard.display "NOISE VIOLATION DETECTED"
}
```

This single `.iot` file models **3 zones, 11 sensors, 8 actuators, and 8 rules** - covering traffic management, environmental hazards, flood response, emergency corridors, lighting automation, and winter road conditions. All of it is validated before deployment and can be exported to JSON, Home Assistant YAML, or a visual diagram with a single CLI command.

---

## Generated Outputs

### JSON (for MQTT / custom runtimes)

```json
{
  "zones": [
    {
      "name": "TrafficDistrict",
      "sensors": [
        { "name": "TrafficDensitySensor", "type": "inductive_loop", "unit": "vehicles_per_minute" },
        { "name": "EmergencyVehicleSensor", "type": "acoustic", "unit": "boolean" }
      ],
      "actuators": [
        { "name": "TrafficLight", "type": "rgb_signal" },
        { "name": "VariableSpeedSign", "type": "led_display" },
        { "name": "EmergencyCorridorSystem", "type": "relay" }
      ]
    }
  ],
  "rules": [
    {
      "name": "EmergencyCorridorActivation",
      "priority": "critical",
      "condition": {
        "sensor": "EmergencyVehicleSensor",
        "attribute": "state",
        "op": "==",
        "value": "active"
      },
      "actions": [
        { "actuator": "EmergencyCorridorSystem", "command": "activate" },
        { "actuator": "TrafficLight", "command": "set_mode", "param": "emergency", "delay_seconds": 2 }
      ]
    }
  ]
}
```

### Home Assistant YAML

```yaml
automation:
  - alias: EmergencyCorridorActivation
    trigger:
      - platform: state
        entity_id: sensor.emergency_vehicle_sensor
        to: "active"
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.emergency_corridor_system
      - delay: "00:00:02"
      - service: light.turn_on
        target:
          entity_id: light.traffic_light
        data:
          effect: emergency

  - alias: NightLighting
    trigger:
      - platform: time
        at: "20:00:00"
    condition:
      - condition: numeric_state
        entity_id: sensor.ambient_light_sensor
        below: 50
    action:
      - service: light.turn_on
        target:
          entity_id: light.street_lighting
```

### Graphviz Diagram

Running `iotflow generate examples/smart_city.iot --target dot` produces a topology diagram showing zones, devices, and rule connections - useful for documentation and system review.

---

## Simulation

IoTFlow includes an event-driven simulator that fires rules against a sequence of mock sensor events, producing a rule execution trace.

```bash
iotflow simulate examples/smart_city.iot --events examples/smart_city_events.json
```

Example output:

```
[00:00] TrafficDensitySensor = 65, EmergencyVehicleSensor = inactive
  → RULE FIRED: HeavyTrafficResponse
    → TrafficLight.set_mode slow
    → VariableSpeedSign.display "CONGESTION - 30km/h"

[00:05] EmergencyVehicleSensor = active
  → RULE FIRED: EmergencyCorridorActivation [CRITICAL]
    → EmergencyCorridorSystem.activate
    → TrafficLight.set_mode emergency [after 2s]
  ⚠ CONFLICT DETECTED: HeavyTrafficResponse also targets TrafficLight
    → Resolved by priority: EmergencyCorridorActivation wins

[00:10] AirQualitySensor = 160
  → RULE FIRED: AirPollutionAlert
    → PollutionAlarm.trigger
    → PublicDisplayBoard.display "HIGH POLLUTION - LIMIT OUTDOOR ACTIVITY"
```

The simulator detects and reports **rule conflicts** - cases where two rules target the same actuator with different commands - and resolves them using declared priority levels.

---

## CLI Reference

```bash
# Validate a model
iotflow validate examples/smart_city.iot

# Parse and inspect model structure
iotflow parse examples/smart_city.iot

# Generate JSON configuration
iotflow generate examples/smart_city.iot --target json

# Generate Home Assistant YAML
iotflow generate examples/smart_city.iot --target homeassistant

# Generate topology diagram
iotflow generate examples/smart_city.iot --target dot

# Run simulation with event trace
iotflow simulate examples/smart_city.iot --events examples/smart_city_events.json
```

---

## Examples

The `examples/` directory contains a range of IoTFlow DSL demonstrations:

| File | Description |
|---|---|
| `basic.iot` | Single sensor and actuator - minimal working model |
| `multi_sensor.iot` | Multiple sensors with coordinated rules |
| `complex_rules.iot` | All comparison operators, AND/OR logic, priorities |
| `home_automation.iot` | Multi-room home automation with time-based rules |
| `smart_greenhouse.iot` | Agricultural IoT - temperature, humidity, soil, CO2 |
| `smart_city.iot` | **Flagship example** - traffic, environment, infrastructure |
| `edge_cases.iot` | Grammar boundary testing and naming conventions |
| `validation_test.iot` | Intentional errors for testing semantic validation |

---

## Project Structure

```
iotflow-dsl/
├── iotflow/
│   ├── grammar/           # textX grammar definition (.tx)
│   ├── validators/        # Semantic validation logic
│   ├── generators/
│   │   ├── json_generator.py
│   │   ├── homeassistant_generator.py
│   │   └── dot_generator.py
│   ├── simulator/         # Event-driven rule simulator
│   ├── cli.py             # IoTFlow CLI entry point
│   └── language.py        # Language registration for textX
├── examples/              # Sample .iot models and event files
├── tests/                 # Unit tests for validators, generators, simulator
├── docs/                  # Editor setup and additional documentation
├── .github/workflows/     # CI - lint and test on push
├── pyproject.toml
└── README.md
```

---

## Editor Support

IoTFlow DSL supports Language Server Protocol (LSP) integration via textX-LS:

- Syntax highlighting for `.iot` files in VS Code
- Real-time validation and inline error reporting
- Auto-complete for device types, actuator commands, and rule keywords

See [Editor Setup Instructions](docs/editor-setup.md) for configuration details.

---

## Installation

```bash
git clone https://github.com/0101dusica/iotflow-dsl.git
cd iotflow-dsl

python -m venv venv
source venv/bin/activate

pip install -e .
pip install textX[cli]
```

Verify:

```bash
textx list-languages
textx list-generators
```

---

## License

MIT - see [LICENSE](LICENSE) for details.

---

## Author

R2 26/2025 Dušica Trbović  
Master Studies - Software Engineering