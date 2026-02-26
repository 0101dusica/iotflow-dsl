# IoTFlow DSL Examples

This directory contains example IoTFlow DSL model files that demonstrate the core language features.

## Available Examples

### `basic.iot`
A minimal example showing the basic structure of IoTFlow DSL:
- Single temperature sensor (DHT22)
- Single actuator (Fan)  
- Simple rule with temperature threshold

**Demonstrates:**
- Basic sensor/actuator definitions
- Simple property assignment (type, unit)
- Basic conditional rule with comparison operator

### `multi_sensor.iot`
Extended example with multiple sensors and actuators:
- 3 sensors: TemperatureSensor, HumiditySensor, MotionDetector
- 3 actuators: Fan, Heater, AlarmBuzzer
- 3 rules for different scenarios

**Demonstrates:**
- Multiple devices of the same type
- Different sensor types (DHT22, PIR)
- Different actuator types (relay, buzzer)
- Multiple rules operating independently

### `complex_rules.iot`
Example focusing on different comparison operators:
- Pressure and light sensors
- Pump and LED actuators
- Rules using all supported operators: `<=`, `>=`, `<`, `!=`

**Demonstrates:**
- Different comparison operators in rules
- Various sensor types (BMP180, LDR)
- Complex actuator control scenarios

### `home_automation.iot`
Real-world home automation scenario:
- Indoor/outdoor temperature monitoring
- Window sensor security
- Thermostat and blind control
- Security system integration

**Demonstrates:**
- Complete automation system
- Multiple temperature sensors
- Security device integration
- Smart home device types

## Validating Examples

Test any example using the IoTFlow CLI:

```bash
python -m iotflow.cli validate examples/<example_name>.iot
```

View parsed model details:

```bash
python -m iotflow.cli parse examples/<example_name>.iot
```

## Language Features Demonstrated

- **Sensor definitions** with type and unit properties
- **Actuator definitions** with type properties  
- **Rule definitions** with when-then structure
- **Comparison operators**: `>`, `<`, `>=`, `<=`, `==`, `!=`
- **Multiple device types** and configurations
- **Cross-references** between sensors, actuators and rules