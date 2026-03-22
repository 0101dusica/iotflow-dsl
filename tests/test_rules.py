import pytest

from iotflow.parser.parse import parse_str
from iotflow.runtime.runner import run_simulation


def _make_dsl(operator, threshold):
    return f'''
    sensor Temp {{
        type: DHT22
        unit: celsius
    }}
    actuator Fan {{
        type: relay
    }}
    rule TestRule {{
        when Temp.value {operator} {threshold}
        then Fan.turn_on
    }}
    '''


@pytest.mark.parametrize("operator,value,threshold,expected", [
    (">", 35.0, 30, True),
    (">", 25.0, 30, False),
    ("<", 25.0, 30, True),
    ("<", 35.0, 30, False),
    (">=", 30.0, 30, True),
    (">=", 29.0, 30, False),
    ("<=", 30.0, 30, True),
    ("<=", 31.0, 30, False),
    ("==", 30.0, 30, True),
    ("==", 31.0, 30, False),
    ("!=", 31.0, 30, True),
    ("!=", 30.0, 30, False),
])
def test_comparison_operators(operator, value, threshold, expected):
    dsl = _make_dsl(operator, threshold)
    model = parse_str(dsl)
    result = run_simulation(model, sensor_overrides={"Temp": value})

    rule_exec = result.cycles[0].rule_executions[0]
    assert rule_exec.condition_met is expected


def test_boundary_value_gt_not_triggered():
    """condition > 30 with value exactly 30 should NOT trigger"""
    dsl = _make_dsl(">", 30)
    model = parse_str(dsl)
    result = run_simulation(model, sensor_overrides={"Temp": 30.0})
    assert result.cycles[0].rule_executions[0].condition_met is False


def test_multiple_rules_same_sensor():
    dsl = r'''
    sensor Temp {
        type: DHT22
        unit: celsius
    }
    actuator Fan { type: relay }
    actuator Heater { type: relay }
    rule CoolDown {
        when Temp.value > 30
        then Fan.turn_on
    }
    rule WarmUp {
        when Temp.value < 15
        then Heater.turn_on
    }
    '''
    model = parse_str(dsl)

    # High temp: only CoolDown triggers
    result = run_simulation(model, sensor_overrides={"Temp": 35.0})
    execs = result.cycles[0].rule_executions
    assert execs[0].condition_met is True   # CoolDown
    assert execs[1].condition_met is False  # WarmUp

    # Low temp: only WarmUp triggers
    result = run_simulation(model, sensor_overrides={"Temp": 10.0})
    execs = result.cycles[0].rule_executions
    assert execs[0].condition_met is False  # CoolDown
    assert execs[1].condition_met is True   # WarmUp
