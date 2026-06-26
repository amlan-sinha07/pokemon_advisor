import os
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
def get_pokemon_moves(pokemon_name:str)-> list:
    moves_path = f"data/moves_{pokemon_name.lower()}.json"

    if os.path.exists(moves_path):
        with open(moves_path, "r",encoding="utf-8") as f:
            cached_data = json.load(f)
            if cached_data is not None:
                return cached_data 
    
    print(f"fetching moves for {pokemon_name}...")
    from scraper.fetch_data import fetch_moves_for_pokemon
    moves = fetch_moves_for_pokemon(pokemon_name.lower())

    if moves is None:
        print(
            f" Error:Could not fetch pokemon moves for {pokemon_name}. Check your scraper or internet connection"

        )
        return []
    with open(moves_path,"w",encoding="utf-8") as f:
        json.dump(moves,f,indent=2)

    return moves
def load_pokemon_with_moves(name:str)->Pokemon:
    pokemon = load_pokemon_fuzzy(name)
    if not pokemon:
        return None
    
    raw_moves = get_pokemon_moves(name.lower())

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
def get_move(move_name: str)->dict:
    import glob
    move_name_clean = move_name.lower().replace(" ","-")

    for filepath in glob.glob("data/moves_*.json"):
        with open(filepath,"r",encoding="utf-8") as f:
            moves = json.load(f)
        for move in moves:
            if move["name"] == move_name_clean:
                return move
        
        print(f"fetching move data for {move_name}...")
        url= f"https://pokeapi.co/api/v2/move/{move_name_clean}"
        
        import requests
        response=requests.get(url)
        if response.status_code != 200:
            return None
        data=response.json()

        effect = ""

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
            #data["effect_entries"][0]["short_effect"]
             #        if data["effect_entries"] else ""
        }
def get_move_fuzzy(move_name:str)->dict:
    from difflib import get_close_matches
    import glob
    move_name_clean = move_name.lower().replace(" ","-")

    all_moves_names=[]
    for filepath in glob.glob("data/moves_*.json"):
        with open(filepath,"r",encoding="utf-8") as f:
            moves=json.load(f)
        for move in moves:
            if move["name"] not in all_moves_names:
                all_moves_names.append(move["name"])

    if move_name_clean in all_moves_names:
        return get_move(move_name_clean)

    matches=get_close_matches(move_name_clean,
                              all_moves_names,
                              n=5,
                              cutoff=0.5)
    if not matches:
        return get_move(move_name_clean)

    if len(matches) ==1:
        print(f"assuming move:{matches[0]}")
        return get_move(matches[0])
    print("did you mean:")
    for i,m in enumerate(matches):
        print(f" {i+1}.{m}")
    choice=input=input("choose (1-5): ").strip()
    try:
        return get_move(matches[int(choice)-1])
    except:
        return get_move(matches[0])        