import warnings

import pytest
from textx.exceptions import TextXSemanticError

from iotflow.parser.parse import parse_str


# --- Existing checks ---

def test_unknown_sensor_reference_raises():
    dsl = r'''
    sensor RealSensor { type: DHT22 unit: celsius }
    actuator Fan { type: relay }
    rule BadRule {
        when NonExistentSensor.value > 30
        then Fan.turn_on
    }
    '''
    with pytest.raises(TextXSemanticError) as exc:
        parse_str(dsl)
    assert "Unknown sensor" in str(exc.value)
    assert "NonExistentSensor" in str(exc.value)


def test_unknown_actuator_reference_raises():
    dsl = r'''
    sensor Temp { type: DHT22 unit: celsius }
    actuator RealActuator { type: relay }
    rule BadRule {
        when Temp.value > 30
        then NonExistentActuator.turn_on
    }
    '''
    with pytest.raises(TextXSemanticError) as exc:
        parse_str(dsl)
    assert "Unknown actuator" in str(exc.value)
    assert "NonExistentActuator" in str(exc.value)


def test_invalid_action_name_raises():
    dsl = r'''
    sensor Temp { type: DHT22 unit: celsius }
    actuator Fan { type: relay }
    rule BadRule {
        when Temp.value > 30
        then Fan.fly_away
    }
    '''
    with pytest.raises(TextXSemanticError) as exc:
        parse_str(dsl)
    assert "Invalid actuator action" in str(exc.value)
    assert "fly_away" in str(exc.value)


def test_valid_model_passes_validation():
    dsl = r'''
    sensor Temp { type: DHT22 unit: celsius }
    actuator Fan { type: relay }
    rule CoolDown {
        when Temp.value > 30
        then Fan.turn_on
    }
    '''
    model = parse_str(dsl)
    assert len(model.elements) == 3


# --- Duplicate name detection ---

def test_duplicate_sensor_name_raises():
    dsl = r'''
    sensor Temp { type: DHT22 unit: celsius }
    sensor Temp { type: SHT30 unit: celsius }
    actuator Fan { type: relay }
    rule R { when Temp.value > 30 then Fan.turn_on }
    '''
    with pytest.raises(TextXSemanticError) as exc:
        parse_str(dsl)
    assert "Duplicate sensor name" in str(exc.value)
    assert "Temp" in str(exc.value)


def test_duplicate_actuator_name_raises():
    dsl = r'''
    sensor Temp { type: DHT22 unit: celsius }
    actuator Fan { type: relay }
    actuator Fan { type: servo }
    rule R { when Temp.value > 30 then Fan.turn_on }
    '''
    with pytest.raises(TextXSemanticError) as exc:
        parse_str(dsl)
    assert "Duplicate actuator name" in str(exc.value)
    assert "Fan" in str(exc.value)


def test_duplicate_rule_name_raises():
    dsl = r'''
    sensor Temp { type: DHT22 unit: celsius }
    actuator Fan { type: relay }
    rule CoolDown { when Temp.value > 30 then Fan.turn_on }
    rule CoolDown { when Temp.value > 35 then Fan.turn_on }
    '''
    with pytest.raises(TextXSemanticError) as exc:
        parse_str(dsl)
    assert "Duplicate rule name" in str(exc.value)
    assert "CoolDown" in str(exc.value)


def test_sensor_actuator_name_collision_raises():
    dsl = r'''
    sensor Device { type: DHT22 unit: celsius }
    actuator Device { type: relay }
    rule R { when Device.value > 30 then Device.turn_on }
    '''
    with pytest.raises(TextXSemanticError) as exc:
        parse_str(dsl)
    assert "Name collision" in str(exc.value)
    assert "Device" in str(exc.value)


# --- Unused device warnings ---

def test_unused_sensor_warns():
    dsl = r'''
    sensor Temp { type: DHT22 unit: celsius }
    sensor Unused { type: SHT30 unit: celsius }
    actuator Fan { type: relay }
    rule R { when Temp.value > 30 then Fan.turn_on }
    '''
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        parse_str(dsl)
        sensor_warnings = [x for x in w if "Unused sensors" in str(x.message)]
        assert len(sensor_warnings) == 1
        assert "Unused" in str(sensor_warnings[0].message)


def test_unused_actuator_warns():
    dsl = r'''
    sensor Temp { type: DHT22 unit: celsius }
    actuator Fan { type: relay }
    actuator Spare { type: servo }
    rule R { when Temp.value > 30 then Fan.turn_on }
    '''
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        parse_str(dsl)
        act_warnings = [x for x in w if "Unused actuators" in str(x.message)]
        assert len(act_warnings) == 1
        assert "Spare" in str(act_warnings[0].message)


# --- Conflicting rules warning ---

def test_conflicting_rules_warns():
    dsl = r'''
    sensor Temp { type: DHT22 unit: celsius }
    actuator Fan { type: relay }
    rule TurnOn { when Temp.value > 25 then Fan.turn_on }
    rule TurnOff { when Temp.value > 30 then Fan.turn_off }
    '''
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        parse_str(dsl)
        conflict_warnings = [x for x in w if "conflicting" in str(x.message).lower()]
        assert len(conflict_warnings) == 1
        assert "TurnOn" in str(conflict_warnings[0].message)
        assert "TurnOff" in str(conflict_warnings[0].message)


def test_non_conflicting_rules_no_warning():
    dsl = r'''
    sensor Temp { type: DHT22 unit: celsius }
    actuator Fan { type: relay }
    actuator Heater { type: relay }
    rule Cool { when Temp.value > 30 then Fan.turn_on }
    rule Heat { when Temp.value < 15 then Heater.turn_on }
    '''
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        parse_str(dsl)
        conflict_warnings = [x for x in w if "conflicting" in str(x.message).lower()]
        assert len(conflict_warnings) == 0
