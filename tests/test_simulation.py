from iotflow.parser.parse import parse_str
from iotflow.runtime.runner import run_simulation


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


def test_rule_triggers_when_condition_met():
    model = parse_str(DSL)
    result = run_simulation(model, sensor_overrides={"TemperatureSensor": 35.0})

    assert len(result.cycles) == 1
    cycle = result.cycles[0]
    assert cycle.readings["TemperatureSensor"] == 35.0
    assert len(cycle.rule_executions) == 1

    rule_exec = cycle.rule_executions[0]
    assert rule_exec.condition_met is True
    assert rule_exec.actuator_name == "Fan"
    assert rule_exec.action_name == "turn_on"


def test_rule_does_not_trigger_when_condition_not_met():
    model = parse_str(DSL)
    result = run_simulation(model, sensor_overrides={"TemperatureSensor": 25.0})

    assert len(result.cycles) == 1
    cycle = result.cycles[0]

    rule_exec = cycle.rule_executions[0]
    assert rule_exec.condition_met is False
    assert rule_exec.actuator_name is None
    assert rule_exec.action_name is None


def test_multiple_cycles():
    model = parse_str(DSL)
    result = run_simulation(model, sensor_overrides={"TemperatureSensor": 35.0}, cycles=3)

    assert len(result.cycles) == 3
    for cycle in result.cycles:
        assert cycle.actions_triggered == 1


def test_result_has_duration():
    model = parse_str(DSL)
    result = run_simulation(model, sensor_overrides={"TemperatureSensor": 35.0})
    assert result.duration_seconds >= 0.0


def test_result_summary_properties():
    model = parse_str(DSL)
    result = run_simulation(model, sensor_overrides={"TemperatureSensor": 35.0}, cycles=2)

    assert result.total_rules_evaluated == 2
    assert result.total_actions_triggered == 2
    assert result.rules_passed == 2
    assert result.rules_not_triggered == 0


def test_result_str_renders():
    model = parse_str(DSL)
    result = run_simulation(model, sensor_overrides={"TemperatureSensor": 35.0})
    output = str(result)
    assert "IoTFlow Simulation Report" in output
    assert "HighTemperature" in output
