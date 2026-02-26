"""
JSON generator for IoTFlow DSL models.

This module transforms validated IoTFlow DSL models into structured JSON representation.
"""

import json
from pathlib import Path
from typing import Dict, List, Any


def extract_properties(properties: List) -> Dict[str, str]:
    """
    Extract type and unit properties from a properties list.
    
    Args:
        properties: List of property objects (TypeProperty, UnitProperty)
        
    Returns:
        Dictionary with 'type' and optionally 'unit' keys
    """
    result = {}
    
    for prop in properties:
        prop_type = prop.__class__.__name__
        if prop_type == 'TypeProperty':
            result['type'] = prop.value
        elif prop_type == 'UnitProperty':
            result['unit'] = prop.value
    
    return result


def generate_json(model, output_path: str) -> None:
    """
    Generate JSON representation of an IoTFlow DSL model.
    
    Args:
        model: Parsed and validated IoTFlow model object
        output_path: Path where the JSON file will be saved
    """
    # Initialize JSON structure
    data = {
        "sensors": [],
        "actuators": [],
        "rules": []
    }
    
    # Process all elements in the model
    for element in model.elements:
        element_type = element.__class__.__name__
        
        if element_type == 'Sensor':
            # Extract sensor properties
            props = extract_properties(element.properties)
            sensor_data = {
                "name": element.name,
                "type": props.get('type'),
                "unit": props.get('unit')
            }
            data["sensors"].append(sensor_data)
            
        elif element_type == 'Actuator':
            # Extract actuator properties
            props = extract_properties(element.properties)
            actuator_data = {
                "name": element.name,
                "type": props.get('type')
            }
            data["actuators"].append(actuator_data)
            
        elif element_type == 'Rule':
            # Extract rule condition and action
            condition = element.when_clause.condition
            action = element.then_clause.action
            
            rule_data = {
                "name": element.name,
                "condition": {
                    "sensor": condition.sensor_ref.sensor_name,
                    "attribute": "value",  # Currently fixed in grammar
                    "operator": condition.operator,
                    "value": condition.value
                },
                "action": {
                    "actuator": action.actuator_ref.actuator_name,
                    "command": action.action_name
                }
            }
            data["rules"].append(rule_data)
    
    # Ensure output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write JSON to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def model_to_json_string(model) -> str:
    """
    Convert IoTFlow model to JSON string (for in-memory use).
    
    Args:
        model: Parsed and validated IoTFlow model object
        
    Returns:
        JSON string representation of the model
    """
    # Initialize JSON structure
    data = {
        "sensors": [],
        "actuators": [],
        "rules": []
    }
    
    # Process all elements in the model
    for element in model.elements:
        element_type = element.__class__.__name__
        
        if element_type == 'Sensor':
            props = extract_properties(element.properties)
            sensor_data = {
                "name": element.name,
                "type": props.get('type'),
                "unit": props.get('unit')
            }
            data["sensors"].append(sensor_data)
            
        elif element_type == 'Actuator':
            props = extract_properties(element.properties)
            actuator_data = {
                "name": element.name,
                "type": props.get('type')
            }
            data["actuators"].append(actuator_data)
            
        elif element_type == 'Rule':
            condition = element.when_clause.condition
            action = element.then_clause.action
            rule_data = {
                "name": element.name,
                "condition": {
                    "sensor": condition.sensor_ref.sensor_name,
                    "attribute": "value",
                    "operator": condition.operator,
                    "value": condition.value
                },
                "action": {
                    "actuator": action.actuator_ref.actuator_name,
                    "command": action.action_name
                }
            }
            data["rules"].append(rule_data)
    
    return json.dumps(data, indent=4, ensure_ascii=False)