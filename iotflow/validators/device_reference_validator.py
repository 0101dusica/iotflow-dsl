"""
Device reference validator for IoTFlow DSL.

This module implements semantic validation to ensure that rules reference
only existing sensors and actuators defined in the model.
"""

from textx import TextXSemanticError


def validate_device_references(model, metamodel):
    """
    Validate that all device references in rules point to existing devices.
    
    Args:
        model: Parsed IoTFlow model object
        metamodel: The metamodel instance (required by textX processor interface)
        
    Raises:
        TextXSemanticError: If a rule references a non-existing sensor or actuator
    """
    # Collect all defined sensor and actuator names
    sensor_names = set()
    actuator_names = set()
    
    for element in model.elements:
        element_type = element.__class__.__name__
        if element_type == 'Sensor':
            sensor_names.add(element.name)
        elif element_type == 'Actuator':
            actuator_names.add(element.name)
    
    # Validate references in rules
    for element in model.elements:
        if element.__class__.__name__ == 'Rule':
            rule_name = element.name
            
            # Check sensor reference in when clause
            if hasattr(element, 'when_clause') and hasattr(element.when_clause, 'condition'):
                condition = element.when_clause.condition
                if hasattr(condition, 'sensor_ref') and hasattr(condition.sensor_ref, 'sensor_name'):
                    referenced_sensor = condition.sensor_ref.sensor_name
                    if referenced_sensor not in sensor_names:
                        # Get position info for better error message
                        pos_info = ""
                        if hasattr(condition.sensor_ref, '_tx_position'):
                            pos = condition.sensor_ref._tx_position
                            pos_info = f" at position {pos}"
                        
                        raise TextXSemanticError(
                            f"Unknown sensor '{referenced_sensor}' referenced in rule '{rule_name}'{pos_info}. "
                            f"Available sensors: {sorted(sensor_names) if sensor_names else 'none'}"
                        )
            
            # Check actuator reference in then clause  
            if hasattr(element, 'then_clause') and hasattr(element.then_clause, 'action'):
                action = element.then_clause.action
                if hasattr(action, 'actuator_ref') and hasattr(action.actuator_ref, 'actuator_name'):
                    referenced_actuator = action.actuator_ref.actuator_name
                    if referenced_actuator not in actuator_names:
                        # Get position info for better error message
                        pos_info = ""
                        if hasattr(action.actuator_ref, '_tx_position'):
                            pos = action.actuator_ref._tx_position
                            pos_info = f" at position {pos}"
                        
                        raise TextXSemanticError(
                            f"Unknown actuator '{referenced_actuator}' referenced in rule '{rule_name}'{pos_info}. "
                            f"Available actuators: {sorted(actuator_names) if actuator_names else 'none'}"
                        )


def register_validators(metamodel):
    """
    Register all device reference validators with the given metamodel.
    
    Args:
        metamodel: textX metamodel instance
    """
    # Register the device reference validator as a model processor
    metamodel.register_model_processor(validate_device_references)