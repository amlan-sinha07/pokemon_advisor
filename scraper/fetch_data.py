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
def fetch_and_save(pokemon_list:list,output_path:str):
    all_pokemon={}
    total=len(pokemon_list)
    for i , name in enumerate(pokemon_list):
        print(f"fetching {name} ({i+1}/{total})...")
        data=fetch_pokemon(name)
        if data:
            all_pokemon[name.lower()]=data
        time.sleep(0.3)
    os.makedirs(os.path.dirname(output_path),exist_ok=True)
    with open(output_path,"w",encoding="utf-8") as f:
        json.dump(all_pokemon, f ,indent=2)
    print(f"\ndone. saved {len(all_pokemon)} pokemon to {output_path}")

if __name__=="__main__":
    starter_list=[
        "pikachu","charizard","blastoise","venusaur",
        "gengar","machamp","alakazam","gyarados",
        "dragonite","mewtwo"
    ]
    fetch_and_save(starter_list,"data/pokemon.json")