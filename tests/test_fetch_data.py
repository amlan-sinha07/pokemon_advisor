
import pytest

from scraper import fetch_data


def test_api_failure_returns_none(monkeypatch):

    def fake_get(*args, **kwargs):
        raise fetch_data.requests.Timeout("Request timed out")

    monkeypatch.setattr(
        fetch_data.requests,
        "get",
        fake_get
    )

    result = fetch_data._get_json(
        "https://example.com/test"
    )

    assert result is None


def test_fetch_pokemon_failure(monkeypatch):

    monkeypatch.setattr(
        fetch_data,
        "_get_json",
        lambda url: None
    )

    assert fetch_data.fetch_pokemon("pikachu") is None


def test_fetch_move_failure(monkeypatch):

    monkeypatch.setattr(
        fetch_data,
        "_get_json",
        lambda url: None
    )

    assert fetch_data.fetch_move("thunderbolt") is None


def test_fetch_pokemon_stores_id(monkeypatch):

    fake_data = {
        "id": 25,
        "name": "pikachu",
        "types": [
            {"type": {"name": "electric"}}
        ],
        "stats": [
            {"stat": {"name": "hp"}, "base_stat": 35},
            {"stat": {"name": "attack"}, "base_stat": 55},
            {"stat": {"name": "defense"}, "base_stat": 40},
            {"stat": {"name": "special-attack"}, "base_stat": 50},
            {"stat": {"name": "special-defense"}, "base_stat": 50},
            {"stat": {"name": "speed"}, "base_stat": 90}
        ],
        "moves": [
            {"move": {"name": "thunderbolt"}}
        ]
    }

    monkeypatch.setattr(
        fetch_data,
        "_get_json",
        lambda url: fake_data
    )

    result = fetch_data.fetch_pokemon("25")

    assert result["id"] == 25
    assert result["name"] == "pikachu"
    assert result["types"] == ["Electric"]
    assert result["stats"]["hp"] == 35


def test_fetch_moves_missing_pokemon(monkeypatch, tmp_path):

    database = tmp_path / "pokemon_all.json"
    database.write_text("{}", encoding="utf-8")

    monkeypatch.setattr(
        fetch_data,
        "POKEMON_FILE",
        database
    )

    result = fetch_data.fetch_moves_for_pokemon("pikachu")

    assert result is None
