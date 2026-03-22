from pathlib import Path
from textx import metamodel_from_file
from iotflow.model import (
    Model, Sensor, Actuator, TypeProperty, UnitProperty,
    Rule, WhenClause, ThenClause, Condition,
    SensorRef, Action, ActuatorRef,
)
from iotflow.parser.preprocessors import convert_operator_to_enum
from iotflow.validators.device_reference_validator import validate_device_references
from iotflow.validators.rule_validator import (
    validate_rule_logic,
    validate_duplicate_rule_names,
    validate_conflicting_rules,
)

HERE = Path(__file__).resolve().parent.parent
GRAMMAR_PATH = HERE / "grammar" / "iotflow.tx"


def build_metamodel():
    mm = metamodel_from_file(
        str(GRAMMAR_PATH),
        classes=[Model,
            Sensor, Actuator, TypeProperty, UnitProperty,
            Rule, WhenClause, ThenClause, Condition,
            SensorRef, Action, ActuatorRef,
        ],
    )
    mm.register_model_processor(convert_operator_to_enum)
    mm.register_model_processor(validate_device_references)
    mm.register_model_processor(validate_rule_logic)
    mm.register_model_processor(validate_duplicate_rule_names)
    mm.register_model_processor(validate_conflicting_rules)

    return mm
