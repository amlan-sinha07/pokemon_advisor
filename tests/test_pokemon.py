
import pytest

from models.pokemon import Pokemon
from models.move import Move


@pytest.fixture
def pokemon():
    return Pokemon(
        name="Pikachu",
        types=["Electric"],
        moves=[],
        stats={"hp": 35}
    )


def test_pokemon_initialization(pokemon):

    assert pokemon.name == "Pikachu"
    assert pokemon.types == ["Electric"]
    assert pokemon.stats["hp"] == 35
    assert pokemon.current_hp == 35
    assert pokemon.moves == []


def test_pokemon_is_alive(pokemon):

    assert pokemon.is_alive() is True


def test_pokemon_is_not_alive(pokemon):

    pokemon.take_damage(35)

    assert pokemon.is_alive() is False


def test_take_damage(pokemon):

    pokemon.take_damage(10)

    assert pokemon.current_hp == 25


def test_take_damage_cannot_reduce_hp_below_zero(pokemon):

    pokemon.take_damage(100)

    assert pokemon.current_hp == 0

def test_take_damage_rejects_negative_amount(pokemon):

    with pytest.raises(ValueError):
        pokemon.take_damage(-10)

    assert pokemon.current_hp == 35
def test_heal_pokemon(pokemon):

    pokemon.take_damage(15)
    pokemon.heal(10)

    assert pokemon.current_hp == 30


def test_heal_cannot_exceed_max_hp(pokemon):

    pokemon.heal(100)

    assert pokemon.current_hp == 35

def test_heal_rejects_negative_amount(pokemon):

    with pytest.raises(ValueError):
        pokemon.heal(-10)

    assert pokemon.current_hp == 35
def test_learn_move(pokemon):

    move = Move(
        "Thunderbolt",
        "Electric",
        90,
        "Special",
        100
    )

    result = pokemon.learn_move(move)

    assert result is True
    assert len(pokemon.moves) == 1
    assert pokemon.moves[0] is move


def test_pokemon_four_move_limit(pokemon):

    for i in range(4):

        move = Move(
            f"Move{i}",
            "Normal",
            50,
            "Physical",
            100
        )

        pokemon.learn_move(move)

    fifth_move = Move(
        "Extra Move",
        "Normal",
        50,
        "Physical",
        100
    )

    result = pokemon.learn_move(fifth_move)

    assert result is False
    assert len(pokemon.moves) == 4


def test_get_types(pokemon):

    assert pokemon.get_types() == ["Electric"]


def test_pokemon_string_representation(pokemon):

    result = str(pokemon)

    assert result == "Pikachu[Electric]HP: 35/35"
'''Add negative damage and healing tests.'''