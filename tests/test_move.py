
from models.move import Move


def test_move_initialization():

    move = Move(
        "Thunderbolt",
        "Electric",
        90,
        "Special",
        100
    )

    assert move.name == "Thunderbolt"
    assert move.move_type == "Electric"
    assert move.power == 90
    assert move.category == "Special"
    assert move.accuracy == 100


def test_physical_move_is_damaging():

    move = Move(
        "Earthquake",
        "Ground",
        100,
        "Physical",
        100
    )

    assert move.is_damaging() is True


def test_special_move_is_damaging():

    move = Move(
        "Thunderbolt",
        "Electric",
        90,
        "Special",
        100
    )

    assert move.is_damaging() is True


def test_status_move_is_not_damaging():

    move = Move(
        "Thunder Wave",
        "Electric",
        0,
        "Status",
        90
    )

    assert move.is_damaging() is False


def test_zero_power_move_is_not_damaging():

    move = Move(
        "Special Move",
        "Psychic",
        0,
        "Special",
        100
    )

    assert move.is_damaging() is False


def test_move_string_representation():

    move = Move(
        "Thunderbolt",
        "Electric",
        90,
        "Special",
        100
    )

    result = str(move)

    assert "Thunderbolt" in result
    assert "Electric" in result
    assert "Power:90" in result
    assert "Cat:Special" in result
    assert "Acc:100" in result
'''Add case-insensitive category tests.'''