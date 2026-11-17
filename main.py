from data_loader import load_pokemon_fuzzy,get_move_fuzzy
from engine.pre_match_advisor import PreMatchAdvisor
from engine.battle_advisor import BattleAdvisor
from models.move import Move
from box_manager import (
    load_box,
    add_to_box,
    remove_from_box,
    view_box
)
def get_current_hp(pokemon, label: str) -> int:

    max_hp = pokemon.stats["hp"]

    while True:

        try:
            hp = int(input(
                f"{label} current HP (0-{max_hp}): "
            ))

        except ValueError:
            print("Enter a valid integer.")
            continue

        if 0 <= hp <= max_hp:
            return hp

        print(f"HP must be between 0 and {max_hp}.")
def pre_match_mode():
    print("\n=== PRE-MATCH TEAM SELECTOR ===")
    box=load_box()
    if box:
        print(f"loading your saved pokemon ({len(box)}) pokemon")
        my_team=[]
        for name in box:
            pokemon=load_pokemon_fuzzy(name)
            if pokemon:
                my_team.append(pokemon)
                print(f"    added: {pokemon.name}")
        if not my_team:
                    print("No valid Pokemon could be loaded from your box.")
                    return
    else:
        print("no saved box found enter your pokemon manually:")
        my_team=[]
        for i in range(6):
            while True:
                name=input(f"your pokemon {i+1}: ").strip().lower()
                pokemon=load_pokemon_fuzzy(name)
                if pokemon:
                    my_team.append(pokemon)
                    print(f"added : {pokemon.name}")
                    break
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
    advisor = PreMatchAdvisor()
    return advisor.recommend(my_team,opp_team)
def battle_mode():
    # import ipdb; ipdb.set_trace()
    print("\n=== IN-BATTLE MOVE ADVISOR ===")
    my_name = input("your active pokemon: ").strip().lower()
    my_pokemon = load_pokemon_fuzzy(my_name)
    if my_pokemon is None:
        print("Could not load your Pokemon.")
        return
    my_pokemon.current_hp = get_current_hp(
    my_pokemon,
    "Your Pokemon"
)

    opp_name= input("opponent's active Pokemon: ").strip().lower()
    opp_pokemon =load_pokemon_fuzzy(opp_name)
    if opp_pokemon is None:
        print("Could not load opponent Pokemon.")
        return
    opp_pokemon.current_hp = get_current_hp(
        opp_pokemon,
        "Opponent"
    )
    print(f"Enter your 4 moves for {my_pokemon.name}:")
    moves=[]
    for i in range(4):
        while True:
            move_name=input(f"move {i+1}: ").strip()
            print("you entered",move_name)
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
def box_mode():
    while True:
        print("\n=== MY BOX ===")
        print("1. view box")
        print("2. add pokemon")
        print("3. remove pokemon")
        print("4. back")
        print()

        choice=input("\nchoose (1-4): ").strip()

        if choice=="1":
            view_box()
        elif choice=="2":
            name=input("pokemon name:").strip()
            add_to_box(name)
        elif choice=="3":
            view_box()
            name=input("remove which pokemon: ").strip()
            remove_from_box(name)
        elif choice=="4":
            break

def main():
    print("="*45)
    print(" POKEMON CHAMPIONS BATTLE ADVISOR")
    print("="*45)

    while True:
        print("\n1. Pre-match team selector")
        print("2. In-battle move advisor")
        print("3. Manage my box")
        print("4. Exit")

        choice = input ("\nChoose (1-4): ").strip()
        if choice=="1":
            pre_match_mode()
        elif choice=="2":
            battle_mode()
        elif choice=="3":
            box_mode()
        elif choice=="4":
            print("Good luck in your battles!")
            break
        else:
            print("Invalid choice.")
if __name__=="__main__":
    main()
#Add minimum-team handling; remove debug output; add invalid menu handling.