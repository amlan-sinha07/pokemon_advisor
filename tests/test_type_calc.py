import pytest
from engine.type_calc import TypeCalculator

@pytest.fixture
def calculator():
    return TypeCalculator()
def test_fire_against_grass(calculator):
    result=calculator.effectiveness(
        "Fire",
        "Grass"
    )
    assert result==2.0
def test_case_insensitive_lookup(calculator):
    result=calculator.effectiveness(
        "fire",
        "grass"
    )
    assert result==2.0
def test_dual_type_effectiveness(calculator):
    result=calculator.dual_type_effectiveness(
        "Fire",
        "Grass",
        "Steel"
    )
    assert result==4.0
def test_unknown_attacking_type(calculator):
    with pytest.raises(ValueError):
        calculator.effectiveness(
            "UnknownType",
            "Grass"
        )
'''
Good starting coverage; add unknown defending type and malformed chart cases
'''