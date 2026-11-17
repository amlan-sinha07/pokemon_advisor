
import json
import pytest

import data_loader


def test_load_pokemon_data(monkeypatch, tmp_path):

    pokemon_file = tmp_path / "pokemon_all.json"

    expected = {
        "pikachu": {
            "name": "pikachu",
            "types": ["Electric"],
            "stats": {"hp": 35},
            "moves": ["thunderbolt"]
        }
    }

    pokemon_file.write_text(
        json.dumps(expected),
        encoding="utf-8"
    )

    monkeypatch.setattr(
        data_loader,
        "POKEMON_FILE",
        pokemon_file
    )

    assert data_loader._load_pokemon_data() == expected


def test_missing_pokemon_database(monkeypatch, tmp_path):

    missing_file = tmp_path / "missing.json"

    monkeypatch.setattr(
        data_loader,
        "POKEMON_FILE",
        missing_file
    )

    with pytest.raises(FileNotFoundError):
        data_loader._load_pokemon_data()


def test_corrupted_pokemon_database(monkeypatch, tmp_path):

    pokemon_file = tmp_path / "pokemon_all.json"

    pokemon_file.write_text(
        "{invalid json",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        data_loader,
        "POKEMON_FILE",
        pokemon_file
    )

    with pytest.raises(ValueError):
        data_loader._load_pokemon_data()


def test_empty_pokemon_search(monkeypatch):

    monkeypatch.setattr(
        data_loader,
        "_load_pokemon_data",
        lambda: {}
    )

    assert data_loader.search_pokemon("") == []


def test_get_pokemon_moves_from_cache(monkeypatch, tmp_path):

    data_dir = tmp_path

    expected = [
        {
            "name": "thunderbolt",
            "type": "Electric",
            "power": 90,
            "accuracy": 100,
            "damage_class": "Special"
        }
    ]

    cache_file = data_dir / "moves_pikachu.json"

    cache_file.write_text(
        json.dumps(expected),
        encoding="utf-8"
    )

    monkeypatch.setattr(
        data_loader,
        "DATA_DIR",
        data_dir
    )

    assert data_loader.get_pokemon_moves("pikachu") == expected


def test_get_move_from_cache(monkeypatch, tmp_path):

    data_dir = tmp_path

    first_cache = data_dir / "moves_pikachu.json"
    second_cache = data_dir / "moves_charizard.json"

    first_cache.write_text("[]", encoding="utf-8")

    expected = {
        "name": "thunderbolt",
        "type": "Electric",
        "power": 90
    }

    second_cache.write_text(
        json.dumps([expected]),
        encoding="utf-8"
    )

    monkeypatch.setattr(
        data_loader,
        "DATA_DIR",
        data_dir
    )

    result = data_loader.get_move("thunderbolt")

    assert result == expected
'''Add malformed Pokémon records and cache validation.'''