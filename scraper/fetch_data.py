#
#
#
import requests
import json
import os
import time

def fetch_pokemon(name:str)->dict:
    url=f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response=requests.get(url)
    if response.status_code !=200:
        print(f"failed to fetch {name}")
        return None
    data=response.json()
    pokemon={
        "name":data["name"],
        "types":[t["type"]["name"].capitalize()
                 for t in data["types"]],
        "stats": {
            "hp": next (s["base_stat"] for s in data["stats"]
                        if s["stat"]["name"]=="hp"),
            "atk": next(s["base_stat"] for s in data["stats"]
                       if s["stat"]["name"]=="attack"),
            "def": next(s["base_stat"] for s in data["stats"]
                        if s["stat"]["name"]=="defense"),
            "spa": next(s["base_stat"] for s in data["stats"]
                        if s["stat"]["name"]=="special-attack"),
            "spd": next(s["base_stat"] for s in data["stats"]
                        if s["stat"]["name"]=="special-defense"),
            "spe": next(s["base_stat"] for s in data["stats"]
                        if s["stat"]["name"]=="speed"),            
            
        },
        "moves": [m["move"]["name"] for m in data["moves"]]
    }
    return pokemon


def fetch_and_save(pokemon_ids: list, output_path: str):
    all_pokemon = {}
    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                all_pokemon = json.load(f)
            print(f"Found existing data. Loaded {len(all_pokemon)} Pokémon.")
        except json.JSONDecodeError:
            print("Existing file was corrupted or empty. Starting fresh.")

    total = len(pokemon_ids)
    
    for i, p_id in enumerate(pokemon_ids):
        if str(p_id) in all_pokemon or p_id.lower() in all_pokemon:
            continue
            
        print(f"Fetching ID {p_id} ({i+1}/{total})...")
        data = fetch_pokemon(p_id)
        
        if data:
            all_pokemon[data["name"]] = data
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(all_pokemon, f, indent=2)
                
        time.sleep(2)

    print(f"\nDone! Total database size: {len(all_pokemon)} Pokémon.")
def fetch_move(move_name: str)-> dict:
    url=f"https://pokeapi.co/api/v2/move/{move_name.lower().replace(' ','-')}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    data = response.json()

    effect_text = ""
    if data.get("effect_entries"):
        for entry in data["effect_entries"]:
            if entry["language"]["name"] == "en":
                effect_text = entry["short_effect"]
                break

    return {
        "name": data["name"],
        "type": data["type"]["name"].capitalize(),
        "power": data["power"] or 0,
        "accuracy": data["accuracy"] or 0,
        "pp": data["pp"],
        "damage_class": data["damage_class"]["name"].capitalize(),
        "effect": effect_text,
    }
def fetch_moves_for_pokemon(pokemon_name:str) ->list:
    with open("data/pokemon_all.json","r",encoding="utf-8") as f:
        all_pokemon = json.load(f)
    
    if pokemon_name not in all_pokemon:
        print(
            f"Debug Error: '{pokemon_name}' not found in pokemon_all.json keys!"
        )
        print(f"Availbale keys snippet: {list(all_pokemon.keys())[:5]}")
        return []
    
    move_names = all_pokemon[pokemon_name]["moves"][:20]
    moves = []

    print(f"found {len(move_names)} moves to fetch for {pokemon_name}...")
    
    for move_name in move_names:
        print(f"    fetching move: {move_name}...")
        move = fetch_move(move_name)
        
        if move is None:
            print(f"    warning: fetch_move('{move_name}) returned None!")
        
        if move:
            moves.append(move)
        
        time.sleep(0.2)
    
    print(f"succesfully fetched {len(moves)} out of {len(move_names)} moves.")
    return moves
# if __name__ == "__main__":
#     generation_9_max = 1025
#     all_pokemon_ids = [str(i) for i in range(1, generation_9_max + 1)]
    
#     fetch_and_save(all_pokemon_ids, "data/pokemon_all.json")