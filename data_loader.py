import json
from models.pokemon import Pokemon
from models.move import Move
from difflib import get_close_matches

def search_pokemon(partial: str)->list:
    with open("data/pokemon_all.json","r",encoding="utf-8") as f:
        all_pokemon = json.load(f)
    
    all_names= list(all_pokemon.keys())
    matches = get_close_matches(
        partial.lower(),
        all_names,
        n=5,
        cutoff=0.5

    )
    return matches
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
            return load_pokemon(matches[int(choice)-1])
        except:
            return load_pokemon(matches[0]) 

def load_pokemon(name:str)->Pokemon:
    with open("data/pokemon_all.json","r",encoding="utf-8") as f:
        all_pokemon=json.load(f)
    name_input=name.lower().strip()
    pokemon_data =None

    for item in all_pokemon.values():
        if item.get("name","").lower() == name_input:
            pokemon_data = item
            break
    if pokemon_data is None:
        raise ValueError(f"{name} not found in database")
    
    #if name not in all_pokemon:
    #    raise ValueError(f"{name} not found in database")
    #data=all_pokemon[name]
    moves=[Move(m,"Normal",0,"Status",100)
           for m in pokemon_data["moves"][:4]]
    return Pokemon(
        name=pokemon_data["name"].capitalize(),
                  types=pokemon_data["types"],
                  stats=pokemon_data["stats"],
                  moves=moves
    )
def load_all_pokemon()->dict:
    with open("data/pokemon_all.json","r",encoding="utf-8") as f:
        all_pokemon=json.load(f)
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
