"""
IoTFlow DSL language registration for textX.

This module registers the IoTFlow domain-specific language with the textX
ecosystem, enabling its use through standard textX CLI tools.
"""

from textx import language, metamodel_from_file
from pathlib import Path
from .validators.device_reference_validator import register_validators
from .validators.rule_validator import register_rule_validators


@language('iotflow', '*.iot')
def iotflow_language():
    """
    Register IoTFlow DSL language with textX.
    
    This function is called by textX when the language is needed.
    It creates and returns a configured metamodel for IoTFlow DSL.
    
    Returns:
        textX metamodel configured with grammar and validators
    """
    # Get path to grammar file relative to this module
    this_dir = Path(__file__).parent
    grammar_path = this_dir / "grammar" / "iotflow.tx"
    
    # Create metamodel from grammar
    metamodel = metamodel_from_file(str(grammar_path))
    
    # Register semantic validators
    register_validators(metamodel)
    register_rule_validators(metamodel)
    
    return metamodel