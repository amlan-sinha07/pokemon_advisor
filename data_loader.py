import json
import time

from pathlib import Path
from difflib import get_close_matches

from models.pokemon import Pokemon
from models.move import Move

DATA_DIR=Path(__file__).resolve().parent/"data"
POKEMON_FILE=DATA_DIR/"pokemon_all.json"

def _load_pokemon_data() -> dict:
    try:
        with POKEMON_FILE.open("r",encoding="utf-8") as f:
            data=json.load(f)
    except FileNotFoundError as exc:
        raise FileNotFoundError (
            f"Pokemon Database not found: {POKEMON_FILE}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise ValueError (
            f"Pokemon database contain invalid json"
        ) from exc
    if not isinstance(data,dict):
        raise ValueError (
            "Pokemon Database must contain a dictionary"
        )
    return data
def search_pokemon(partial: str)->list[str]:
    all_pokemon=_load_pokemon_data()
    query=partial.strip().lower()
    if not query:
        return []
    all_names= [
        item["name"].strip().lower()
        for item in all_pokemon.values()
        if isinstance(item,dict)
        and isinstance(item.get("name"),str)
    ]
    return get_close_matches(
        query,
        all_names,
        n=5,
        cutoff=0.5
    )
def load_pokemon_fuzzy(name:str):
    try:
        return load_pokemon(name)
    except ValueError:
        matches=search_pokemon(name)
        if not matches:
            print(f"no pokemon found matching '{name}")
            return None
        if len(matches)==1:
            print(f"assuming you meant: {matches[0]}")
            return load_pokemon(matches[0])
        print(f"did you mean:")
        for i, m in enumerate(matches):
            print(f"    {i+1}. {m}")
        choice = input("choose (1-5): ").strip()
        try:
            selected_index=int(choice)-1
        except ValueError:
            print("Invalid selection")
            return None
        if not 0<=selected_index<len(matches):
            print("Selection out of range")
            return None
        return load_pokemon(matches[selected_index])
def load_pokemon(name:str)->Pokemon:
    all_pokemon=_load_pokemon_data()
    name_input=name.strip().lower()
    pokemon_data =None
    for item in all_pokemon.values():
        if not isinstance(item,dict):
            continue
        if item.get("name","").strip().lower() == name_input:
            pokemon_data = item
            break
    if pokemon_data is None:
        raise ValueError(
            f"{name} not found in database"
        )
    moves=[Move(m,"Normal",0,"Status",100)
           for m in pokemon_data["moves"][:4]]
    return Pokemon(
        name=pokemon_data["name"].capitalize(),
        types=pokemon_data["types"],
        stats=pokemon_data["stats"],
        moves=moves
    )
def load_all_pokemon()->dict:
    all_pokemon=_load_pokemon_data()
    result={}
    for name, item in all_pokemon.items():
        pokemon_name= item["name"].lower()
        moves =[Move(m,"Normal",0,"Status",100)
                for m in item["moves"][:4]]
        result[pokemon_name]=Pokemon(
            name=item["name"].capitalize(),
            types=item["types"],
            stats=item["stats"],
            moves=moves
        )
    return result
def get_pokemon_moves(pokemon_name: str) -> list[dict]:
    moves_path = DATA_DIR / f"moves_{pokemon_name.strip().lower()}.json"
    if moves_path.exists():
        with moves_path.open("r", encoding="utf-8") as f:
            cached_data = json.load(f)
        if not isinstance(cached_data, list):
            raise ValueError(
                f"Invalid move cache: {moves_path}"
            )
        return cached_data
    print(f"Fetching moves for {pokemon_name}...")
    from scraper.fetch_data import fetch_moves_for_pokemon
    moves = fetch_moves_for_pokemon(pokemon_name.lower())
    if moves is None:
        print(f"Could not fetch moves for {pokemon_name}.")
        return []
    if not isinstance(moves, list):
        raise ValueError("Fetched move data must be a list.")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with moves_path.open("w", encoding="utf-8") as f:
        json.dump(moves, f, indent=2)
    return moves
def load_pokemon_with_moves(name:str)->Pokemon | None:
    pokemon = load_pokemon_fuzzy(name)
    if not pokemon:
        return None
    raw_moves = get_pokemon_moves(pokemon.name.lower())
    move_objects = []
    for m in raw_moves:
        move = Move(
            name= m["name"],
            move_type=m["type"],
            power=m["power"],
            category=m["damage_class"],
            accuracy=m["accuracy"]
        )
        move_objects.append(move)
    pokemon.moves = move_objects
    return pokemon
def get_move(move_name: str)->dict | None:
    move_name_clean = move_name.lower().replace(" ","-")
    for filepath in DATA_DIR.glob("moves_*.json"):
        with filepath.open("r",encoding="utf-8") as f:
            moves=json.load(f)
        for move_data in moves:
            if move_data.get("name")==move_name_clean:
                return move_data
    print(f"fetching move data for {move_name}")
    import requests
    url= f"https://pokeapi.co/api/v2/move/{move_name_clean}"
    try:
        response=requests.get(url,timeout=10)
        if response.status_code != 200:
            return None
        data=response.json()
    except (requests.RequestException,ValueError) as exc:
        print(f"Could not fetch move data : {exc}")
        return None
    time.sleep(0.2)
    effect=""
    if data.get("effect_entries"):
        for entry in data["effect_entries"]:
            if entry.get("language",{}).get("name") == "en":
                effect = entry.get("short_effect","")
                break
    return {
        "name":data.get("name"),
        "type":data.get("type",{}).get("name","normal").capitalize(),
        "power":data.get("power") or 0,
        "accuracy":data.get("accuracy") or 0,
        "pp":data.get("pp") or 0,
        "damage_class":data.get("damage_class",{}).get("name","Physical").capitalize(),
        "effect": effect
    }
def get_move_fuzzy(move_name:str)->dict | None:
    move_name_clean = move_name.lower().replace(" ","-")
    move=get_move(move_name_clean)
    if move:
        return move
    from difflib import get_close_matches
    import glob
    all_moves_names=[]
    for filepath in DATA_DIR.glob("moves_*.json"):
        with open(filepath,"r",encoding="utf-8") as f:
            moves=json.load(f)
        for move in moves:
            move_name=move.get("name")
            if move_name and move_name not in all_moves_names:
                all_moves_names.append(move_name)
    if not all_moves_names :
        print(f"move {move_name} not found")
        return None
    if move_name_clean in all_moves_names:
        return get_move(move_name_clean)

    matches=get_close_matches(move_name_clean,
                              all_moves_names,
                              n=5,
                              cutoff=0.4)
    if not matches:
        print(f"move {move_name} not found")
        return None
    if len(matches) ==1:
        print(f"assuming move:{matches[0]}")
        return get_move(matches[0])
    print("did you mean:")
    for i,m in enumerate(matches):
        print(f" {i+1}.{m}")
    choice=input("choose (1-5): ").strip()
    try:
        selected_index=int(choice)-1
    except ValueError:
        print("Invalid selection")
        return None
    if not 0<=selected_index<len(matches):
        print("selection out of range")
        return None
    return get_move(matches[selected_index])
'''
Module: data_loader.py

Responsibilities:
- Loads Pokémon entities and moves from local JSON caches or data stores.
- Provides fuzzy matching for Pokémon names and move names using `difflib`.
- Falls back to live network requests (PokéAPI) if move or Pokémon data is missing locally.

Dependencies:
- standard -> os, json, time, glob, difflib
- external -> requests
- internal -> models.pokemon -> Pokemon, models.move -> Move, scraper.fetch_data -> fetch_moves_for_pokemon

Known problems:
- Nested loop bug in `get_move`: the network fetch block is incorrectly indented *inside* the file-reading loop, causing it to prematurely fetch or return on the very first file checked if the move isn't found immediately.
- Global scope import leak: `from data_loader import get_pokemon_moves` at the bottom of the module imports from itself, and `pokemon_to_fetch` is an empty uninitialized list.

Testing:
- No automated tests currently documented.
'''