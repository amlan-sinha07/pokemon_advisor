
import pytest

from engine.pre_match_advisor import PreMatchAdvisor
from models.pokemon import Pokemon


class FakeTypeCalculator:

    def effectiveness(self, attacking_type, defending_type):

        chart = {
            ("fire", "grass"): 2.0,
            ("grass", "fire"): 0.5
        }

        return chart.get(
            (attacking_type.lower(), defending_type.lower()),
            1.0
        )


@pytest.fixture
def advisor(monkeypatch):

    monkeypatch.setattr(
        "engine.pre_match_advisor.TypeCalculator",
        FakeTypeCalculator
    )

    return PreMatchAdvisor()


def create_pokemon(name, types, speed):

    return Pokemon(
        name=name,
        types=types,
        moves=[],
        stats={
            "hp": 100,
            "spe": speed
        }
    )


def test_score_matchup(advisor):

    charmander = create_pokemon("Charmander", ["Fire"], 100)
    bulbasaur = create_pokemon("Bulbasaur", ["Grass"], 80)

    result = advisor.score_matchup(charmander, bulbasaur)

    # Offensive: 2.0
    # Defensive: -(0.5 * 0.5)
    # Speed: +0.5

    assert result == 2.25


def test_score_vs_team(advisor):

    charmander = create_pokemon("Charmander", ["Fire"], 100)

    opponent_team = [
        create_pokemon("Bulbasaur", ["Grass"], 80),
        create_pokemon("Oddish", ["Grass"], 60)
    ]

    result = advisor.score_vs_team(
        charmander,
        opponent_team
    )

    assert result == 4.5


def test_score_vs_empty_team(advisor):

    charmander = create_pokemon("Charmander", ["Fire"], 100)

    result = advisor.score_vs_team(charmander, [])

    assert result == 0.0


def test_recommend_returns_highest_scoring_pokemon(advisor):

    charmander = create_pokemon("Charmander", ["Fire"], 100)
    rattata = create_pokemon("Rattata", ["Normal"], 50)

    opponent_team = [
        create_pokemon("Bulbasaur", ["Grass"], 80)
    ]

    result = advisor.recommend(
        [rattata, charmander],
        opponent_team,
        pick=1
    )

    assert result == [charmander]
