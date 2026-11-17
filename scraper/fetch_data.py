import requests
import json
import time

from pathlib import Path

PROJECT_ROOT=Path(__file__).resolve().parents[1]
DATA_DIR=PROJECT_ROOT / "data"
POKEMON_FILE=DATA_DIR / "pokemon_all.json"
REQUEST_TIMEOUT=10
def _get_json(url:str)->dict|None:
    try:
        response=requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        data=response.json()
    except (requests.RequestException, ValueError) as exc:
        print(f"API requests failed: {exc}")
        return None
    if not isinstance(data,dict):
        print("API returned unexpected json data")
        return None
    return data
def fetch_pokemon(name:str)->dict | None:
    identifier=str(name).strip().lower()
    url=f"https://pokeapi.co/api/v2/pokemon/{identifier}"
    data=_get_json(url)
    if data is None:
        return None
    stat_mapping={
        "hp":"hp",
        "attack":"atk",
        "defense":"def",
        "special-attack":"spa",
        "special-defense":"spd",
        "speed":"spe"
    }
    stats={}
    for item in data.get("stats",[]):
        api_name=item.get("stat",{}).get("name")
        if api_name in stat_mapping:
            stats[stat_mapping[api_name]]=item["base_stat"]
    required_stats={"hp","atk","def","spa","spd","spe"}
    if not required_stats.issubset(stats):
        print(f"Incomplete stats for {identifier}")
        return None
    pokemon_name=data.get("name")
    if not isinstance(pokemon_name,str) or not pokemon_name:
        return None
    return {
        "id":data.get("id"),
        "name":pokemon_name,
        "types":[
            item["type"]["name"].capitalize()
            for item in data.get("types",[])
        ],
        "stats":stats,
        "moves":[
            item["move"]["name"]
            for item in data.get("moves",[])
        ]
    }
def fetch_and_save(
        pokemon_ids: list,
        output_path: str | Path
    ) -> None :
    output_file=Path(output_path)
    if not output_file.is_absolute():
        output_file=PROJECT_ROOT/output_file
    all_pokemon = {}
    if output_file.exists():
        try:
            with output_file.open("r", encoding="utf-8") as f:
                all_pokemon = json.load(f)
            if not isinstance(all_pokemon,dict):
                raise ValueError("Database must be dictionary.")
            print(
                f"Found existing data. Loaded {len(all_pokemon)} Pokémon."
            )
        except (json.JSONDecodeError,ValueError):
            print("Existing file was corrupted or empty. Starting fresh.")
            all_pokemon={}
    cached_ids=set()
    cached_names={
        str(name).lower()
        for name in all_pokemon
    }
    for item in all_pokemon.values():
        if isinstance(item,dict) and item.get("id") is not None:
            cached_ids.add(str(item["id"]))
    total = len(pokemon_ids)
    pending_saves=0
    output_file.parent.mkdir(parents=True,exist_ok=True)
    for i, p_id in enumerate(pokemon_ids):
        identifier=str(p_id).strip().lower()
        if identifier in cached_ids or identifier in cached_names:
            continue
        print(f"Fetching ID {p_id} ({i+1}/{total})...")
        data = fetch_pokemon(p_id)
        if data:
            all_pokemon[data["name"]] = data
            cached_names.add(data["name"].lower())
            if data.get("id") is not None:
                cached_ids.add(str(data["id"]))
            pending_saves += 1
        if pending_saves>=25:
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(all_pokemon, f, indent=2)
            pending_saves=0
        time.sleep(2)
    if pending_saves > 0 :
        with output_file.open("w",encoding="utf-8") as f:
            json.dump(all_pokemon,f,indent=2)
    print(
        f"\nDone! Total database size: {len(all_pokemon)} Pokémon."
    )
def fetch_move(move_name: str)-> dict | None:
    move_slug=move_name.strip().lower().replace(" ","-")
    url=f"https://pokeapi.co/api/v2/move/{move_slug}"
    data=_get_json(url)
    if data is None:
        return None
    effect_text = ""
    for entry in data.get("effect_entries",[]):
        if entry.get("language",{}).get("name")=="en":
            effect_text=entry.get("short_effect","")
            break
    return {
        "name": data["name"],
        "type": data.get("type",{}).get("name","normal").capitalize(),
        "power": data.get("power") or 0,
        "accuracy": data.get("accuracy") or 0,
        "pp": data.get("pp") or 0,
        "damage_class": data.get(
            "damage_class",{}
        ).get("name","physical").capitalize(),
        "effect": effect_text,
    }
def fetch_moves_for_pokemon(
        pokemon_name:str
    ) ->list[dict] | None:
    try :
        with POKEMON_FILE.open("r",encoding="utf-8") as f:
            all_pokemon=json.load(f)
    except (FileNotFoundError,json.JSONDecodeError) as exc:
        print(f"Could not load Pokemon database: {exc}")
        return None
    if not isinstance(all_pokemon,dict):
        return None
    name=pokemon_name.strip().lower()
    pokemon_data=all_pokemon.get(name)
    if not isinstance(pokemon_data,dict):
        print(f"pokemon '{name}' not found or invalid.")
        return None
    all_move_names=pokemon_data.get("moves",[])
    if not isinstance(all_move_names,list):
        print("Invalid moves data in Pokemon database")
        return None
    move_names=all_move_names[:20]
    moves=[]
    print(f"Found {len(move_names)} moves for {name}...")
    for move_name in move_names:
        print(f"Fetching move: {move_name}")
        move=fetch_move(move_name)
        if move is not None :
            moves.append(move)
        time.sleep(0.2)
    print(
        f"Successfully fetched {len(moves)}"
        f"out of {len(move_names)} moves."
    )
    return moves
"""
Module: fetch_data.py

Responsibilities:
- Fetch Pokemon metadata from PokeAPI.
- Fetch individual move details.
- Normalize API responses into application data structures.
- Maintain the local Pokemon JSON database.
- Cache move information through the data-loading layer.
- Handle request failures and API timeouts.

Dependencies:
- External: requests
- Standard: json, time, pathlib

Known limitations:
- Uses individual HTTP requests rather than a shared requests.Session.
- Move retrieval is limited to the first 20 available moves.
- PokeAPI availability does not establish Pokemon Champions compatibility.

Testing:
- Covered by tests/test_fetch_data.py.
"""