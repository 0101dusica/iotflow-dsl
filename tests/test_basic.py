from iotflow.parser.parse import parse_str
from iotflow.model import Sensor, Actuator, Rule, TypeProperty, UnitProperty
from iotflow.runtime.context import build_context


DSL = r'''
sensor TemperatureSensor {
    type: DHT22
    unit: celsius
}

actuator Fan {
    type: relay
}

rule HighTemperature {
    when TemperatureSensor.value > 30
    then Fan.turn_on
}
'''


def test_parse_basic_model():
    model = parse_str(DSL)
    assert len(model.elements) == 3
    assert isinstance(model.elements[0], Sensor)
    assert isinstance(model.elements[1], Actuator)
    assert isinstance(model.elements[2], Rule)


def test_sensor_properties():
    model = parse_str(DSL)
    sensor = model.elements[0]
    assert sensor.name == "TemperatureSensor"
    assert len(sensor.properties) == 2

    type_props = [p for p in sensor.properties if isinstance(p, TypeProperty)]
    unit_props = [p for p in sensor.properties if isinstance(p, UnitProperty)]
    assert len(type_props) == 1
    assert type_props[0].value == "DHT22"
    assert len(unit_props) == 1
    assert unit_props[0].value == "celsius"


def test_actuator_properties():
    model = parse_str(DSL)
    actuator = model.elements[1]
    assert actuator.name == "Fan"
    assert len(actuator.properties) == 1
    assert isinstance(actuator.properties[0], TypeProperty)
    assert actuator.properties[0].value == "relay"


def test_rule_structure():
    model = parse_str(DSL)
    rule = model.elements[2]
    assert rule.name == "HighTemperature"
    assert rule.when_clause is not None
    assert rule.when_clause.condition.sensor_ref.sensor_name == "TemperatureSensor"
    assert rule.when_clause.condition.value == 30
    assert rule.then_clause.action.actuator_ref.actuator_name == "Fan"
    assert rule.then_clause.action.action_name == "turn_on"


def test_context_building():
    model = parse_str(DSL)
    ctx = build_context(model)
    assert "TemperatureSensor" in ctx.sensors
    assert "Fan" in ctx.actuators
    assert len(ctx.rules) == 1
    assert ctx.rules[0].name == "HighTemperature"


def test_model_with_only_sensor():
    dsl = r'''
    sensor Temp { type: DHT22 unit: celsius }
    '''
    model = parse_str(dsl)
    assert len(model.elements) == 1
    assert isinstance(model.elements[0], Sensor)


def test_multiple_sensors_and_rules():
    dsl = r'''
    sensor TempSensor { type: DHT22 unit: celsius }
    sensor HumiditySensor { type: DHT22 unit: percent }
    actuator Fan { type: relay }
    actuator Heater { type: relay }
    rule CoolDown {
        when TempSensor.value > 30
        then Fan.turn_on
    }
    rule WarmUp {
        when TempSensor.value < 15
        then Heater.turn_on
    }
    '''
    model = parse_str(dsl)
    ctx = build_context(model)
    assert len(ctx.sensors) == 2
    assert len(ctx.actuators) == 2
    assert len(ctx.rules) == 2
