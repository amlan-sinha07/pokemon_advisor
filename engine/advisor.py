#
#
#
from engine.type_calc import TypeCalculator
from engine.damage_calc import DamageCalculator
from models.pokemon import Pokemon

class PreMatchAdvisor:
    def __init__(self):
        self.type_calc=TypeCalculator()
        self.damage_calc=DamageCalculator()
    def score_matchup(self,my_pokemon:Pokemon,
                      opponent:Pokemon)->float:
        score=0.0

        #offensive score
        for my_type in my_pokemon.types:
            for opp_type in opponent.types:
                effectiveness= self.type_calc.effectiveness(
                    my_type, opp_type
                )
                score += effectiveness
        #defensive score
        for opp_type in opponent.types:
            for my_type in my_pokemon.types:
                incoming= self.type_calc.effectiveness(
                    opp_type,my_type
                )
                score -= incoming *0.5
        #speed bonus
        if my_pokemon.stats["spe"]>opponent.stats["spe"]:
            score += 0.5
        
        return round(score ,2)
    def score_vs_team(self,my_pokemon:Pokemon,
                      opponent_team:list)->float:
        total=0.0
        for opponent in opponent_team:
            total += self.score_matchup(my_pokemon,opponent)
        return round(total,2)
    def recommend(self, my_team:list,
                  opponent_team:list,pick=4)->list:
        scores=[]
        for pokemon in my_team:
            score = self.score_vs_team(pokemon,opponent_team)
            scores.append((pokemon, score))
        scores.sort(key=lambda x:x[1],reverse =True)

        print("\n=== PRE-MATCH ANALYSIS ===")
        print(f"\nOpponent's team:")
        for opp in opponent_team:
            print(f" {opp.name} [{'/'.join(opp.types)}]")
        
        print(f"\nYour team score:")
        for pokemon ,score in scores:
            print(f" {pokemon.name:<12} "
                  f"[{'/'.join(pokemon.types):<15}] "
                  f"score:{score}")
            
        print(f"\n>>> BRING THESE {pick} POKEMON <<<")
        recommended = []
        for pokemon , score in scores[:pick]:
            print(f" {pokemon.name} (score: {score})")
            recommended.append(pokemon)
        return recommended
        