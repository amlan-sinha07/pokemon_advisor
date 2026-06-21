import json
from models.pokemon import Pokemon
from models.move import Move

def load_pokemon(name:str)->Pokemon:
    with open("data/pokemon.json","r",encoding="utf-8") as f:
        all_pokemon=json.load(f)
    name=name.lower()
    if name not in all_pokemon:
        raise ValueError(f"{name} not found in database")
    data=all_pokemon[name]
    moves=[Move(m,"Normal",0,"Status",100)
           for m in data["moves"][:4]]
    return Pokemon(
        name=data["name"].capitalize(),
                  types=data["types"],
                  stats=data["stats"],
                  moves=moves
    )
def load_all_pokemon()->dict:
    with open("data/pokemon.json","r",encoding="utf-8") as f:
        all_pokemon=json.load(f)
    result={}
    for name, data in all_pokemon.items():
        moves =[Move(m,"Normal",0,"Status",100)
                for m in data["moves"][:4]]
        result[name]=Pokemon(
            name=data["name"].capitalize(),
            types=data["types"],
            stats=data["stats"],
            moves=moves
        )
    return result
