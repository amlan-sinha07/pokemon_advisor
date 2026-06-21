from data_loader import load_pokemon, load_all_pokemon
p=load_pokemon("pikachu")
print(p)
print(p.types)
print(p.stats)

p2=load_pokemon("gyarados")
print(p2)
print(p2.types)