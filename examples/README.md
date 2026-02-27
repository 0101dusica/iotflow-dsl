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

### `smart_greenhouse.iot`
Complex IoT system for greenhouse management:
- Multiple environmental sensors (temperature, humidity, CO2, light)
- Coordinated climate control actuators
- Irrigation management system
- Advanced lighting control

**Demonstrates:**
- Large-scale IoT system design
- Multiple sensor types working together
- Complex automation scenarios
- Real-world agricultural IoT application

### `validation_test.iot`
Test file containing intentional errors for LSP validation testing:
- Invalid sensor references
- Missing syntax elements
- Typos in operators
- Duplicate definitions

**Demonstrates:**
- How textX-LS reports validation errors
- Common syntax mistakes
- Error detection capabilities
- Inline error reporting in VS Code

### `edge_cases.iot`
Grammar boundary testing and naming conventions:
- Various naming styles (camelCase, snake_case, UPPERCASE)
- Extreme threshold values
- All comparison operators
- Minimal and maximal identifier lengths

**Demonstrates:**
- Grammar flexibility and limits
- Different naming conventions
- Edge case value handling
- Comprehensive operator testing

## Testing textX-LS Integration

For testing Language Server Protocol integration, use these specific examples:

### `validation_test.iot`
Open this file in VS Code with textX-LS configured to see:
- Red underlines on invalid syntax
- Error messages in the Problems panel  
- Real-time validation as you type
- Hover tooltips with error details

### `edge_cases.iot`
Use this file to test grammar boundaries and ensure:
- Various naming conventions are supported
- Edge case values are handled correctly
- All comparison operators work properly
- Complex scenarios are parsed correctly

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
- **Comments and documentation** within DSL files
- **Naming conventions** (camelCase, snake_case, UPPERCASE)
- **Edge case handling** (extreme values, minimal identifiers)
- **Error validation** and LSP integration testing
- **Complex system modeling** with multiple coordinated devices

## Example Progression

For learning IoTFlow DSL, follow this recommended order:

1. **`basic.iot`** - Start here to understand core concepts
2. **`multi_sensor.iot`** - Learn multiple device handling  
3. **`complex_rules.iot`** - Explore all comparison operators
4. **`home_automation.iot`** - See realistic application
5. **`smart_greenhouse.iot`** - Study complex system design
6. **`edge_cases.iot`** - Test advanced features
7. **`validation_test.iot`** - Understand error handling