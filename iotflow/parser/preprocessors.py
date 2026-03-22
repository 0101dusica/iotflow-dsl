from textx import get_children_of_type
from iotflow.model import Condition, ComparisonOp


def convert_operator_to_enum(model, _) -> None:
    for cond in get_children_of_type(Condition, model):
        op = cond.operator
        if isinstance(op, str):
            cond.operator = ComparisonOp(op)
