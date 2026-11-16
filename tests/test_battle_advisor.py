
import pytest

from engine.battle_advisor import BattleAdvisor
from models.pokemon import Pokemon
from models.move import Move


class FakeDamageCalculator:

    def calculate(self, attacker, defender, move):

        damage_values = {
            "Thunderbolt": 90,
            "Quick Attack": 40
        }

        return {
            "damage": damage_values[move.name],
            "effectiveness": 1.0,
            "note": "test calculation"
        }


@pytest.fixture
def advisor(monkeypatch):

    monkeypatch.setattr(
        "engine.battle_advisor.DamageCalculator",
        FakeDamageCalculator
    )

    return BattleAdvisor()


@pytest.fixture
def battle_pokemon():

    attacker = Pokemon(
        name="Pikachu",
        types=["Electric"],
        moves=[],
        stats={"hp": 100, "spe": 110}
    )

    defender = Pokemon(
        name="Charizard",
        types=["Fire", "Flying"],
        moves=[],
        stats={"hp": 150, "spe": 100}
    )

    return attacker, defender


def test_recommend_highest_damage_move(advisor, battle_pokemon):

    attacker, defender = battle_pokemon

    moves = [
        Move("Quick Attack", "Normal", 40, "Physical", 100),
        Move("Thunderbolt", "Electric", 90, "Special", 100)
    ]

    result = advisor.recommend_move(
        attacker,
        defender,
        moves
    )

    assert result["move"].name == "Thunderbolt"
    assert result["damage"] == 90


def test_status_move_is_not_sent_to_damage_calculator(
    advisor,
    battle_pokemon
):

    attacker, defender = battle_pokemon

    moves = [
        Move("Thunder Wave", "Electric", 0, "Status", 90)
    ]

    result = advisor.recommend_move(
        attacker,
        defender,
        moves
    )

    assert result["move"].name == "Thunder Wave"
    assert result["damage"] == 0
    assert result["note"] == "status move"
def test_empty_moves_returns_none(advisor, battle_pokemon):

    attacker, defender = battle_pokemon

    result = advisor.recommend_move(
        attacker,
        defender,
        []
    )

    assert result is None