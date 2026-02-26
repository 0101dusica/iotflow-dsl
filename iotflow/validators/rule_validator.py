"""
Rule logic validator for IoTFlow DSL.

This module implements semantic validation to ensure rule conditions 
and actions are structurally correct and logically valid.
"""

from textx import TextXSemanticError


# Valid operators for condition comparisons
VALID_OPERATORS = {">", "<", ">=", "<=", "==", "!="}

# Valid action names for actuators
VALID_ACTIONS = {
    "turn_on", "turn_off", "activate", "deactivate", "start", "stop",
    "open", "close", "set", "adjust", "reset", "emergency_stop",
    "reduce_power", "set_heating", "alert", "adjust_brightness"
}

# Valid sensor attributes that can be accessed
VALID_SENSOR_ATTRIBUTES = {"value"}


def validate_rule_logic(model, metamodel):
    """
    Validate that all rules have correct condition operators, numeric values,
    and valid actuator actions.
    
    Args:
        model: Parsed IoTFlow model object
        metamodel: The metamodel instance (required by textX processor interface)
        
    Raises:
        TextXSemanticError: If a rule has invalid logic
    """
    for element in model.elements:
        if element.__class__.__name__ == 'Rule':
            rule_name = element.name
            
            # Validate condition in when clause
            if hasattr(element, 'when_clause') and hasattr(element.when_clause, 'condition'):
                condition = element.when_clause.condition
                
                # 1. Validate operator
                if hasattr(condition, 'operator'):
                    operator = condition.operator
                    if operator not in VALID_OPERATORS:
                        # Get position info for error
                        pos_info = ""
                        if hasattr(condition, '_tx_position'):
                            pos = condition._tx_position
                            pos_info = f" at position {pos}"
                        
                        raise TextXSemanticError(
                            f"Invalid operator '{operator}' in rule '{rule_name}'{pos_info}. "
                            f"Valid operators: {sorted(VALID_OPERATORS)}"
                        )
                
                # 2. Validate comparison value is numeric
                if hasattr(condition, 'value'):
                    value = condition.value
                    if not isinstance(value, (int, float)):
                        # Get position info for error
                        pos_info = ""
                        if hasattr(condition, '_tx_position'):
                            pos = condition._tx_position
                            pos_info = f" at position {pos}"
                        
                        raise TextXSemanticError(
                            f"Condition value must be numeric in rule '{rule_name}'{pos_info}. "
                            f"Found: {type(value).__name__} '{value}'"
                        )
            
            # Validate action in then clause
            if hasattr(element, 'then_clause') and hasattr(element.then_clause, 'action'):
                action = element.then_clause.action
                
                # 3. Validate action name
                if hasattr(action, 'action_name'):
                    action_name = action.action_name
                    if action_name not in VALID_ACTIONS:
                        # Get position info for error
                        pos_info = ""
                        if hasattr(action, '_tx_position'):
                            pos = action._tx_position
                            pos_info = f" at position {pos}"
                        
                        raise TextXSemanticError(
                            f"Invalid actuator action '{action_name}' in rule '{rule_name}'{pos_info}. "
                            f"Valid actions: {sorted(VALID_ACTIONS)}"
                        )


def register_rule_validators(metamodel):
    """
    Register all rule logic validators with the given metamodel.
    
    Args:
        metamodel: textX metamodel instance
    """
    # Register the rule logic validator as a model processor
    metamodel.register_model_processor(validate_rule_logic)