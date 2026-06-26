from engine.damage_calc import DamageCalculator
from data_loader import load_pokemon
from models.move import Move

# # # # calc=DamageCalculator()

# # # # pikachu=load_pokemon("pikachu")
# # # # gyarados=load_pokemon("gyarados")
# # # # mewtwo=load_pokemon("mewtwo")

# # # # thunderbolt =Move("Thunderbolt","Electric",90,"Special",100)
# # # # earthquake =Move("Earthquake","Ground",100,"Physical",100)
# # # # psychic =Move("Psychic","Psychic",90,"Special",100)

# # # # result=calc.calculate(pikachu ,gyarados ,thunderbolt)
# # # # print(f"Thunderbolt vs Gyarados: {result}")

# # # # result2=calc.calculate(pikachu, gyarados, earthquake)
# # # # print(f"Earthquake vs Gyarados: {result2}")

# # # # result3=calc.calculate(mewtwo,mewtwo,psychic)
# # # # print(f"Psychic vs Mewtwo: {result3}")

from engine.type_calc import TypeCalculator
# # # # calc = TypeCalculator()
# # # # print(calc.effectiveness("Psychic", "Psychic"))  # should be 0.5
# # # # mewtwo = load_pokemon("mewtwo")
# # # # print(mewtwo.types)
# # # # print(mewtwo.stats)

# # # # # add this debug to main.py temporarily
# # # # mewtwo = load_pokemon("mewtwo")
# # # # psychic = Move("Psychic", "Psychic", 90, "Special", 100)

# # # # print(f"attacker types: {mewtwo.types}")
# # # # print(f"move type: {psychic.move_type}")
# # # # print(f"defender types: {mewtwo.types}")

# # # # # check STAB
# # # # stab = 1.5 if psychic.move_type in mewtwo.types else 1.0
# # # # print(f"stab: {stab}")

# # # # # check effectiveness
# # # # from engine.type_calc import TypeCalculator
# # # # tc = TypeCalculator()
# # # # effectiveness = 1.0
# # # # for defend_type in mewtwo.types:
# # # #     e = tc.effectiveness(psychic.move_type, defend_type)
# # # #     print(f"effectiveness vs {defend_type}: {e}")
# # # #     effectiveness *= e
# # # # print(f"total effectiveness: {effectiveness}")
# # # #
# # # #
# # # #
from engine.advisor import PreMatchAdvisor
from data_loader import load_pokemon

# advisor = PreMatchAdvisor()

# my_team= [
#     load_pokemon("azumarill"),
#     load_pokemon("corviknight"),
#     load_pokemon("froslass"),
#     load_pokemon("lucario"),
#     load_pokemon("decidueye"),
#     load_pokemon("araquanid")
# ]
# opponent_team=[
#     load_pokemon(""),
#     load_pokemon("gardevoir"),
#     load_pokemon("headavross"),
#     load_pokemon("grampa"),
#     load_pokemon("corviknight"),
#     load_pokemon("azumarill")
# ]

# advisor.recommend(my_team,opponent_team)
# # #
# # #
# # #
from engine.battle_advisor import BattleAdvisor
from data_loader import load_pokemon
from models.move import Move

# # advisor= BattleAdvisor()

# # pikachu = load_pokemon("pikachu")
# # gyarados = load_pokemon("gyarados")

# # #simulate HP loss
# # pikachu.take_damage(10)
# # gyarados.take_damage(40)

# # #pikachu's 4 moves
# # moves = [
# #     Move("Thunderbolt" , "Electric",90,"Special",100),
# #     Move("iron Tail","steel",100,"physical",75),
# #     Move("Quick attack","Normal",40,"Physical",100),
# #     Move("Thunder Wave","Electric",0,"Status",90),
# # ]
# # advisor.recommend_move(pikachu, gyarados,moves)

from engine.advisor import PreMatchAdvisor
from engine.battle_advisor import BattleAdvisor
from data_loader import load_pokemon_fuzzy,load_pokemon
from data_loader import search_pokemon
from models.move import Move

def pre_match_mode():
    print("\n=== PRE-MATCH TEAM SELECTOR ===")
    print("Enter your 6 Pokemon (partial names ok):")
    my_team=[]
    for i in range(6):
        while True:
            name = input(f"your pokemon {i+1}: ").strip().lower()
            pokemon=load_pokemon_fuzzy(name)
            if pokemon:
                my_team.append(pokemon)
                print(f"    added: {pokemon.name}")
                break
            # try:
            #     my_team.append(load_pokemon_fuzzy(name))
            #     break
            # except ValueError:
            #     print(f"'{name}' not found. try again.")
    print("\nEnter opponent's 6 Pokemon (one per line):")
    opp_team = []
    for i in range(6):
        while True:
            name = input(f" Opponent Pokemon {i+1}: ").strip().lower()
            pokemon=load_pokemon_fuzzy(name)
            if pokemon:
                opp_team.append(pokemon)
                print(f" added: {pokemon.name}")
                break
            # try:
            #     opp_team.append(load_pokemon_fuzzy(name))
            #     break
            # except ValueError:
            #     print(f" '{name}' not found. try again.")
    advisor = PreMatchAdvisor()
    return advisor.recommend(my_team,opp_team)
def battle_mode():
    print("\n=== IN-BATTLE MOVE ADVISOR ===")
    my_name = input("your active pokemon: ").strip().lower()
    my_pokemon = load_pokemon_fuzzy(my_name)
    my_hp= int(input(f" Current Hp (max {my_pokemon.stats['hp']}): "))
    my_pokemon.current_hp = my_hp

    opp_name= input("opponent's active Pokemon: ").strip().lower()
    opp_pokemon =load_pokemon_fuzzy(opp_name)
    opp_hp = int(input(f" opponent's current hp (max{opp_pokemon.stats['hp']}): "))
    opp_pokemon.current_hp = opp_hp

    print("\nYour 4 moves: ")
    moves=[]
    move_data = [
        ("Thunderbolt","Electric",90,"Special",100),
        ("Iron Tail","Steel",100,"Physical",75),
        ("Quick Attack","Normal",40,"Physical",100),
        ("Thunder Wave","Electric",0,"Status",90),
    ]
    for name, mtype , power , cat, acc in move_data:
        moves.append(Move(name, mtype, power,cat ,acc))
    advisor = BattleAdvisor()
    advisor.recommend_move(my_pokemon, opp_pokemon, moves)
def main():
    print("="*45)
    print(" POKEMON CHAMPIONS BATTLE ADVISOR")
    print("="*45)

    while True:
        print("\n1. Pre-match team selector")
        print("2. In-battle move advisor")
        print("3.exit")

        choice = input ("\nChoose (1-3): ").strip()
        if choice=="1":
            pre_match_mode()
        elif choice=="2":
            battle_mode()
        elif choice=="3":
            print("Good luck in your battles!")
            break
        else:
            print("Invalid choice.")
# print(search_pokemon("azuma"))
# print(search_pokemon("corvi"))
# print(search_pokemon("frolss"))
# print(search_pokemon("snow"))
# print(search_pokemon("luca"))
if __name__=="__main__":
    main()
from data_loader import load_pokemon_with_moves

# scizor=load_pokemon_with_moves("scizor")
# print(scizor)
# print(f"\n{scizor.name}'s moves:")
# for move in scizor.moves[:5]:
#     print(f"{move}")
# gyarados =load_pokemon("gyarados")
# print(gyarados.stats)
from engine.damage_calc import DamageCalculator
from data_loader import load_pokemon
#from models.move import Move

# calc = DamageCalculator()
# pikachu= load_pokemon("pikachu")
# gyarados = load_pokemon("gyarados")
# thunderbolt=Move("Thunderbolt","Electric",90,"Special",100)

# result = calc.calculate(pikachu,gyarados,thunderbolt)
# print(result)
from data_loader import get_move_fuzzy

# m=get_move_fuzzy("thunderbolt")
# print(m)

# m2= get_move_fuzzy("earthquake")
# print(m2)

# m3= get_move_fuzzy("thunder")
# print(m3)
from data_loader import load_pokemon,load_pokemon_fuzzy,get_move_fuzzy
def battle_mode():
    print("\n=== IN-BATTLE MOVE ADVISOR ===")
    my_name=input("your active pokemon: ").strip()
    my_pokemon=load_pokemon_fuzzy(my_name)
    if not my_pokemon:
        return
    my_hp=int(input(f"current hp (max{my_pokemon.stats['hp']}): "))
    my_pokemon.current_hp=my_hp

    opp_name=input("opponent's active pokemon: ").strip()
    opp_pokemon=load_pokemon_fuzzy(opp_name)
    if not opp_pokemon:
        return
    opp_hp=int(input(f"opponent hp (max {opp_pokemon.stats['hp']}): \n"))
    opp_pokemon.current_hp=opp_hp

    print(f"Enter your 4 moves for {my_pokemon.name}:")
    moves=[]
    for i in range(4):
        while True:
            move_name=input(f"move {i+1}: ").strip()
            if not move_name:
                continue
            move_data=get_move_fuzzy(move_name)
            if move_data:
                move=Move(
                    name=move_data["name"],
                    move_type=move_data["type"],
                    power=move_data["power"],
                    category=move_data["damage_class"],
                    accuracy=move_data["accuracy"]
                )
                moves.append(move)
                print(f" added: {move.name}"
                      f"[{move.move_type}]"
                      f"power:{move.power}")
                break
            else:
                print(f" move {move_name} not found . try again.")
    advisor =BattleAdvisor()
    advisor.recommend_move(my_pokemon,opp_pokemon,moves)