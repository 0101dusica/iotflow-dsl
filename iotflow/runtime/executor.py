from dataclasses import dataclass
from typing import Optional

from ..model import Rule
from .evaluator import evaluate_condition


@dataclass
class RuleExecution:
    rule_name: str
    sensor_name: str
    sensor_value: float
    condition_met: bool
    actuator_name: Optional[str] = None
    action_name: Optional[str] = None


def execute_rules(
    rules: list[Rule],
    readings: dict[str, float],
) -> list[RuleExecution]:
    results: list[RuleExecution] = []

    for rule in rules:
        sensor_name = rule.when_clause.condition.sensor_ref.sensor_name
        sensor_value = readings.get(sensor_name, 0.0)

        try:
            condition_met = evaluate_condition(rule.when_clause.condition, readings)
        except RuntimeError:
            condition_met = False

        execution = RuleExecution(
            rule_name=rule.name,
            sensor_name=sensor_name,
            sensor_value=sensor_value,
            condition_met=condition_met,
        )

        if condition_met:
            execution.actuator_name = rule.then_clause.action.actuator_ref.actuator_name
            execution.action_name = rule.then_clause.action.action_name

        results.append(execution)

    return results
