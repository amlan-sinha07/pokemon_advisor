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

if __name__ == "__main__":
    generation_9_max = 1025
    all_pokemon_ids = [str(i) for i in range(1, generation_9_max + 1)]
    
    fetch_and_save(all_pokemon_ids, "data/pokemon_all.json")