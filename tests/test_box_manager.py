import json
import pytest

import box_manager

@pytest.fixture
def box_path(tmp_path,monkeypatch):
    path=tmp_path/"my_box.json"
    monkeypatch.setattr(
        box_manager,
        "box_file",
        path
    )
    return path
def test_load_missing_box(box_path):
    assert box_manager.load_box()==[]
def test_save_and_load(box_path):
    expected=["pikachu","charizard"]
    box_manager.save_box(expected)
    assert box_manager.load_box()==expected
def test_load_corrupted_json(box_path):
    box_path.write_text(
        "invalid json",
        encoding="utf-8"
    )
    with pytest.raises(ValueError):
        box_manager.load_box()
def test_load_invalid_json_structure(box_path):
    box_path.write_text(
        '{"pokemon":"pikachu"}',
        encoding="utf-8"
    )
    with pytest.raises(ValueError):
        box_manager.load_box()
def test_add_pokemon(box_path):
    box_manager.add_to_box("Pikachu")
    assert box_manager.load_box()==["pikachu"]
def test_duplicate_pokemon(box_path):
    box_manager.save_box(["pikachu"])
    box_manager.add_to_box("pikachu")
    assert box_manager.load_box()==["pikachu"]
def test_box_capacity(box_path):
    pokemon=[
        "pikachu",
        "charizard",
        "lucario",
        "gengar",
        "greninja",
        "dragonite"
    ]
    box_manager.save_box(pokemon)
    box_manager.add_to_box("garchomp")
    assert box_manager.load_box()==pokemon
    assert len(box_manager.load_box())==6
def test_remove_pokemon(box_path):
    box_manager.save_box(["pikachu","charizard"])
    box_manager.remove_from_box("pikachu")
    assert box_manager.load_box()==["charizard"]
def test_save_box_rejects_more_than_six(box_path):

    pokemon = [f"pokemon_{i}" for i in range(7)]

    with pytest.raises(ValueError):
        box_manager.save_box(pokemon)


def test_load_box_rejects_more_than_six(box_path):

    pokemon = [f"pokemon_{i}" for i in range(7)]

    box_path.write_text(
        json.dumps(pokemon),
        encoding="utf-8"
    )

    with pytest.raises(ValueError):
        box_manager.load_box()
'''
Capacity test ineffective
'''