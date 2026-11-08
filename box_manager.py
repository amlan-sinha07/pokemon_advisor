import json
import os

from data import my_box as box_file

def load_box() -> list:
    if not os.path.exists(box_file):
        return []
    with open(box_file,"r",encoding="utf-8") as f:
        return json.load(f)

def save_box(box:list):
    with open(box_file,"w",encoding="utf-8") as f:
        json.dump(box, f, indent=2)
    print(f"box saved . {len(box)} pokemon in your box")

def add_to_box(pokemon_name: str):
    box=load_box()
    name=pokemon_name.lower().strip()
    if name in box:
        print(f"{name} is already in your box.")
        return
    if len(box)>=6:
        print("box is full (6/6). remove a pokemon first.")
        return
    box.append(name)
    save_box(box)
    print(f"added {name} to the box. ({len(box)}/6)")

def remove_from_box(pokemon_name:str):
    box=load_box()
    name=pokemon_name.lower().strip()
    if name not in box:
        print(f"{name} not in box")
        return
    box.remove(name)
    save_box(box)
    print(f"removed {name}. ({len(box)}/6)")

def view_box():
    box=load_box()
    if not box:
        print("box is empty")
        return
    print(f"\n=== YOUR BOX ({len(box)}/6) ===")
    for i , name in enumerate(box):
        print(f"    {i+1}.  {name}")
'''
Module: box_manager.py

Responsibilities:
- Manages local Pokémon team/box storage (persisting, loading, adding, removing, and viewing team members).
- Enforces team size limits (max 6 Pokémon).

Dependencies:
- standard -> json, os

Known problems:
- `load_box()` lacks `json.JSONDecodeError` handling; if `my_box.json` is empty or corrupted, the program will crash.
- Tight coupling of persistence logic with UI output (`print` inside `save_box`).
- Hardcoded relative path (`my_box.json`) can cause file-not-found errors if run from a different working directory.

Testing:
- No automated tests currently documented.
'''