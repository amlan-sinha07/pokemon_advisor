#
#
#
from models.pokemon import Pokemon
from models.move import Move
from engine.type_calc import TypeCalculator

class DamageCalculator:
    def __init__(self):
        self.type_calc=TypeCalculator()
    def calculate(self,attacker:Pokemon,defender:Pokemon,
                  move:Move)->dict:
        if not move.is_damaging():
            return {"damage":0,"effectiveness":1.0,"note":"status move"}
        stab=1.5 if move.move_type in attacker.types else 1.0
        effectiveness=1.0
        for defend_type in defender.types:
            effectiveness *= self.type_calc.effectiveness(
                move.move_type,defend_type
            )
        if move.category=="Physical":
            atk=attacker.stats["atk"]
            def_=defender.stats["def"]
        else:
            atk=attacker.stats["spa"]
            def_=defender.stats["spd"]
        damage=((2*50/5+2)* move.power * atk/ def_)/50+2
        damage *= stab  *effectiveness
        if effectiveness ==0:
            note="no effect"
        elif effectiveness <1:
            note="not very effective"
        elif effectiveness==1:
            note="super effective"
        else:
            note="double super effective"
        #print(f"DEBUG: stab={stab}, effectiveness={effectiveness}, power={move.power}, atk={atk}, def_={def_}")
        #print(f"DEBUG: raw damage before stab/effectiveness = {((2 * 50 / 5 + 2) * move.power * atk / def_) / 50 + 2}")
        #print(f"DEBUG: final = {((2 * 50 / 5 + 2) * move.power * atk / def_) / 50 + 2} * {stab} * {effectiveness}")
        return {
            "damage":round(damage),
            "effectiveness":effectiveness,
            "stab":stab,
            "note":note
        }
    