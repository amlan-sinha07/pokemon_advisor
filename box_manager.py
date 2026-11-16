import json
import os
from pathlib import Path

MAX_BOX_SIZE=6

box_file=Path(__file__).resolve().parent/"my_box.json"

def load_box() -> list:
    try:
        with box_file.open("r",encoding="utf-8") as f:
            box=json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid json in saved box : {box_file}"
        ) from exc
    if not isinstance(box,list):
        raise ValueError("saved pokemon box must contain a list")
    if len(box)>MAX_BOX_SIZE:
        return ValueError("Saved pokemon box exceed the maximum size")
    if any(
        not isinstance(name,str) or not name.strip()
        for name in box
    ):
        raise ValueError("saved box contain an invalid pokemon")
    return box
def save_box(box:list[str]) -> None:
    if not isinstance(box,list):
        raise ValueError("saved pokemon box must contain a list")
    if len(box)>MAX_BOX_SIZE:
        return ValueError("Saved pokemon box exceed the maximum size")
    if any(
        not isinstance(name,str) or not name.strip()
        for name in box
    ):
        raise ValueError("pokemon name must be non-empty string")
    with open(box_file,"w",encoding="utf-8") as f:
        json.dump(box, f, indent=2)
def add_to_box(pokemon_name: str):
    box=load_box()
    name=pokemon_name.strip().lower()
    if not name:
        print("pokemon name can not be empty")
        return
    if name in box:
        print(f"{name} is already in your box.")
        return
    if len(box)>=MAX_BOX_SIZE:
        print("box is full (6/6). remove a pokemon first.")
        return
    box.append(name)
    save_box(box)
    print(f"added {name} to the box. ({len(box)}/6)")

def remove_from_box(pokemon_name:str)->None:
    box=load_box()
    name=pokemon_name.strip().lower()
    if not name:
        print("Pokemon name can not be empty")
        return
    if name not in box:
        print(f"{name} not in box")
        return
    box.remove(name)
    save_box(box)
    print(f"removed {name}. ({len(box)}/6)")
def view_box()->None:
    box=load_box()
    if not box:
        print("box is empty")
        return
    print(f"\n=== YOUR BOX ({len(box)}/6) ===")
    for i , name in enumerate(box):
        print(f"    {i+1}.  {name}")
"""
Module: box_manager.py

Responsibilities:
- Load and save the local Pokemon box.
- Add and remove Pokemon.
- Display saved Pokemon.
- Enforce the maximum box size.

Dependencies:
- json
- pathlib

Testing:
- Covered by tests/test_box_manager.py.
"""