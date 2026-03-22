import operator as op_module

from ..model import Condition, ComparisonOp

_OPS = {
    ComparisonOp.GT:  op_module.gt,
    ComparisonOp.LT:  op_module.lt,
    ComparisonOp.GTE: op_module.ge,
    ComparisonOp.LTE: op_module.le,
    ComparisonOp.EQ:  op_module.eq,
    ComparisonOp.NEQ: op_module.ne,
}


def evaluate_condition(condition: Condition, readings: dict[str, float]) -> bool:
    sensor_name = condition.sensor_ref.sensor_name
    if sensor_name not in readings:
        raise RuntimeError(f"No reading for sensor '{sensor_name}'")
    current = readings[sensor_name]
    comparator = _OPS[condition.operator]
    return comparator(current, condition.value)
