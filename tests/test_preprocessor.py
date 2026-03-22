import pytest

from iotflow.parser.parse import parse_str
from iotflow.model import Rule, ComparisonOp


DSL = r'''
sensor Temp {
    type: DHT22
    unit: celsius
}

actuator Fan {
    type: relay
}

rule TestRule {
    when Temp.value > 30
    then Fan.turn_on
}
'''


def test_operator_is_enum_after_parse():
    model = parse_str(DSL)

    rules = [el for el in model.elements if isinstance(el, Rule)]
    assert len(rules) == 1

    condition = rules[0].when_clause.condition
    assert isinstance(condition.operator, ComparisonOp)
    assert condition.operator == ComparisonOp.GT


@pytest.mark.parametrize("op_str,expected_enum", [
    (">", ComparisonOp.GT),
    ("<", ComparisonOp.LT),
    (">=", ComparisonOp.GTE),
    ("<=", ComparisonOp.LTE),
    ("==", ComparisonOp.EQ),
    ("!=", ComparisonOp.NEQ),
])
def test_each_operator_converted(op_str, expected_enum):
    dsl = f'''
    sensor S {{ type: DHT22 unit: celsius }}
    actuator A {{ type: relay }}
    rule R {{
        when S.value {op_str} 30
        then A.turn_on
    }}
    '''
    model = parse_str(dsl)
    rules = [el for el in model.elements if isinstance(el, Rule)]
    assert rules[0].when_clause.condition.operator == expected_enum
