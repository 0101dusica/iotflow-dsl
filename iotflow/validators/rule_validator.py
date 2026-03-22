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
                    # After preprocessor, operator may be a ComparisonOp enum
                    op_str = operator.value if hasattr(operator, 'value') else operator
                    if op_str not in VALID_OPERATORS:
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


OPPOSITE_ACTIONS = {
    "turn_on": "turn_off",
    "turn_off": "turn_on",
    "activate": "deactivate",
    "deactivate": "activate",
    "start": "stop",
    "stop": "start",
    "open": "close",
    "close": "open",
}


def validate_conflicting_rules(model, metamodel):
    """
    Detect rules that may conflict: two rules targeting the same actuator
    with opposite actions where their conditions can overlap.
    """
    rules = []
    for element in model.elements:
        if element.__class__.__name__ == 'Rule':
            if (hasattr(element, 'when_clause') and hasattr(element.when_clause, 'condition')
                    and hasattr(element, 'then_clause') and hasattr(element.then_clause, 'action')):
                cond = element.when_clause.condition
                act = element.then_clause.action
                sensor_name = cond.sensor_ref.sensor_name if hasattr(cond, 'sensor_ref') else None
                operator = cond.operator
                op_str = operator.value if hasattr(operator, 'value') else operator
                value = cond.value if hasattr(cond, 'value') else None
                actuator_name = act.actuator_ref.actuator_name if hasattr(act, 'actuator_ref') else None
                action_name = act.action_name if hasattr(act, 'action_name') else None
                rules.append((element.name, sensor_name, op_str, value, actuator_name, action_name))

    import warnings
    for i, (name_a, sensor_a, op_a, val_a, act_a, action_a) in enumerate(rules):
        for name_b, sensor_b, op_b, val_b, act_b, action_b in rules[i + 1:]:
            if act_a != act_b or sensor_a != sensor_b:
                continue
            if OPPOSITE_ACTIONS.get(action_a) != action_b:
                continue
            if _conditions_can_overlap(op_a, val_a, op_b, val_b):
                warnings.warn(
                    f"Potentially conflicting rules: '{name_a}' and '{name_b}' "
                    f"target the same actuator '{act_a}' with opposite actions "
                    f"('{action_a}' vs '{action_b}') and their conditions on "
                    f"sensor '{sensor_a}' can overlap.",
                    stacklevel=2,
                )


def _conditions_can_overlap(op_a, val_a, op_b, val_b):
    """Check if two conditions on the same sensor can be true simultaneously."""
    if val_a is None or val_b is None:
        return True

    # > X and < Y overlap when Y > X
    # > X and > Y always overlap (some value satisfies both)
    gt_ops = {">", ">="}
    lt_ops = {"<", "<="}

    if op_a in gt_ops and op_b in gt_ops:
        return True
    if op_a in lt_ops and op_b in lt_ops:
        return True
    if op_a in gt_ops and op_b in lt_ops:
        return val_b > val_a
    if op_a in lt_ops and op_b in gt_ops:
        return val_a > val_b
    if op_a == "==" or op_b == "==":
        return True
    if op_a == "!=" or op_b == "!=":
        return True
    return True


def validate_duplicate_rule_names(model, metamodel):
    """
    Detect duplicate rule names.
    """
    rule_names = set()
    for element in model.elements:
        if element.__class__.__name__ == 'Rule':
            if element.name in rule_names:
                raise TextXSemanticError(
                    f"Duplicate rule name '{element.name}'. "
                    f"Each rule must have a unique name."
                )
            rule_names.add(element.name)


def register_rule_validators(metamodel):
    """
    Register all rule logic validators with the given metamodel.

    Args:
        metamodel: textX metamodel instance
    """
    metamodel.register_model_processor(validate_rule_logic)
    metamodel.register_model_processor(validate_duplicate_rule_names)
    metamodel.register_model_processor(validate_conflicting_rules)