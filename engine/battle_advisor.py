#
#
from engine.damage_calc import DamageCalculator
from models.pokemon import Pokemon
from models.move import Move

class BattleAdvisor:
    def __init__(self):
        self.damage_calc= DamageCalculator()
    def recommend_move(self,attacker:Pokemon,
                       defender:Pokemon,
                       moves:list)->dict:
        print(f"\n=== BATTLE ADVISOR ===")
        print(f"Your : {attacker.name} "
              f"HP: {attacker.current_hp}/{attacker.stats['hp']}")
        print(f"Opponent: {defender.name} "
              f"HP: {defender.current_hp}/{defender.stats['hp']}")
        #speed check
        # speed check
        if attacker.stats["spe"] > defender.stats["spe"]:
            print(f"⚡ You go FIRST (spd {attacker.stats['spe']} "
                  f"> {defender.stats['spe']})")
        elif attacker.stats["spe"] < defender.stats["spe"]:
            print(f"⚠️  Opponent goes FIRST (spd {defender.stats['spe']} "
                  f"> {attacker.stats['spe']})")
        else:
            print(f"⚖️  Same speed — 50/50")
        
        # score each move
        results=[]
        for move in moves:
            if not move.is_damaging():
                results.append({
                    "move":move,
                    "damage":0,
                    "effectiveness":1.0,
                    "note":"status move"
                })
                continue
            result= self.damage_calc.calculate(
                attacker,defender,move
            )
            result["move"]=move
            results.append(result)
        results.sort(key=lambda x : x["damage"], reverse =True)

        print(f"\nMove analysis:")
        for r in results:
            print(f"    {r['move'].name:<16} "
                  f"dmg:{r['damage']:<6} "
                  f"effectiveness: {r['effectiveness']}x "
                  f"({r['note']})")
        best = results[0]
        print(f"\n>>> USE: {best['move'].name} "
              f"({best['note']}, "
              f"~ {best['damage']} damage) <<<")
        return best