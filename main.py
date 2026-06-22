# # from engine.damage_calc import DamageCalculator
# # from data_loader import load_pokemon
# # from models.move import Move

# # calc=DamageCalculator()

# # pikachu=load_pokemon("pikachu")
# # gyarados=load_pokemon("gyarados")
# # mewtwo=load_pokemon("mewtwo")

# # thunderbolt =Move("Thunderbolt","Electric",90,"Special",100)
# # earthquake =Move("Earthquake","Ground",100,"Physical",100)
# # psychic =Move("Psychic","Psychic",90,"Special",100)

# # result=calc.calculate(pikachu ,gyarados ,thunderbolt)
# # print(f"Thunderbolt vs Gyarados: {result}")

# # result2=calc.calculate(pikachu, gyarados, earthquake)
# # print(f"Earthquake vs Gyarados: {result2}")

# # result3=calc.calculate(mewtwo,mewtwo,psychic)
# # print(f"Psychic vs Mewtwo: {result3}")

# # from engine.type_calc import TypeCalculator
# # calc = TypeCalculator()
# # print(calc.effectiveness("Psychic", "Psychic"))  # should be 0.5
# # mewtwo = load_pokemon("mewtwo")
# # print(mewtwo.types)
# # print(mewtwo.stats)

# # # add this debug to main.py temporarily
# # mewtwo = load_pokemon("mewtwo")
# # psychic = Move("Psychic", "Psychic", 90, "Special", 100)

# # print(f"attacker types: {mewtwo.types}")
# # print(f"move type: {psychic.move_type}")
# # print(f"defender types: {mewtwo.types}")

# # # check STAB
# # stab = 1.5 if psychic.move_type in mewtwo.types else 1.0
# # print(f"stab: {stab}")

# # # check effectiveness
# # from engine.type_calc import TypeCalculator
# # tc = TypeCalculator()
# # effectiveness = 1.0
# # for defend_type in mewtwo.types:
# #     e = tc.effectiveness(psychic.move_type, defend_type)
# #     print(f"effectiveness vs {defend_type}: {e}")
# #     effectiveness *= e
# # print(f"total effectiveness: {effectiveness}")
# #
# #
# #
# from engine.advisor import PreMatchAdvisor
# from data_loader import load_pokemon

# advisor = PreMatchAdvisor()

# my_team= [
#     load_pokemon("pikachu"),
#     load_pokemon("charizard"),
#     load_pokemon("blastoise"),
#     load_pokemon("gengar"),
#     load_pokemon("machamp"),
#     load_pokemon("dragonite")
# ]
# opponent_team=[
#     load_pokemon("gyarados"),
#     load_pokemon("alakazam"),
#     load_pokemon("mewtwo"),
#     load_pokemon("dragonite"),
#     load_pokemon("venusaur"),
#     load_pokemon("blastoise")
# ]

# advisor.recommend(my_team,opponent_team)
#
#
#
from engine.battle_advisor import BattleAdvisor
from data_loader import load_pokemon
from models.move import Move

advisor= BattleAdvisor()

pikachu = load_pokemon("pikachu")
gyarados = load_pokemon("gyarados")

#simulate HP loss
pikachu.take_damage(10)
gyarados.take_damage(40)

#pikachu's 4 moves
moves = [
    Move("Thunderbolt" , "Electric",90,"Special",100),
    Move("iron Tail","steel",100,"physical",75),
    Move("Quick attack","Normal",40,"Physical",100),
    Move("Thunder Wave","Electric",0,"Status",90),
]
advisor.recommend_move(pikachu, gyarados,moves)