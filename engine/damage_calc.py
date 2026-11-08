#
#
#
import subprocess
import os
from models.pokemon import Pokemon
from models.move import Move
from engine.type_calc import TypeCalculator

class DamageCalculator:
    def __init__(self):
        self.type_calc=TypeCalculator()
        self.cpp_calc=os.path.join(
            os.path.dirname(__file__),"damage_calc.exe"
        )
    def calculate_cpp(self, power:int, atk:int,
                      def_stat:int,effectiveness:float,
                      stab:float)->int:
        if not os.path.exists(self.cpp_calc):
            return None
        input_str = f"{power} {atk} {def_stat} {effectiveness} {stab}"
        result = subprocess.run(
            [self.cpp_calc],
            input=input_str,
            capture_output=True,
            text=True
        )
        return int(result.stdout.strip())
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
        cpp_result = self.calculate_cpp(
            move.power, atk , def_,effectiveness,stab
        )
        if cpp_result is not None:
            damage = cpp_result
            engine= "C++"
        else:
            damage= ((2*50/5+2)* move.power*atk/def_)/50+2
            damage= round(damage*stab*effectiveness)
            engine= "Python"
        #damage=((2*50/5+2)* move.power * atk/ def_)/50+2
        #damage *= stab  *effectiveness
        if effectiveness ==0:
            note="no effect"
        elif effectiveness ==0.25:
            note ="quad resists"
        elif effectiveness <1:
            note="not very effective"
        elif effectiveness==1:
            note="normal effective"
        elif effectiveness ==2.0:
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
            "note":note,
            "engine":engine
        }
'''
Module: damage_calc.py

Responsibilities:
- Calculates battle damage for Pokémon moves using either a high-performance C++ backend binary (`damage_calc.exe`) or a Python fallback formula.
- Integrates type effectiveness multipliers and Same-Type Attack Bonus (STAB).

Dependencies:
- standard -> subprocess, os
- internal -> models.pokemon -> Pokemon, models.move -> Move, engine.type_calc -> TypeCalculator

Known problems:
- Fragile subprocess communication: `input=input_str` is passed without a trailing newline, which can cause `std::cin` in the C++ binary to hang or fail depending on stream buffering.
- Missing exception handling for subprocess output: `int(result.stdout.strip())` will crash with a `ValueError` if the C++ executable prints warning logs, debug text, or returns malformed data.
- Lacks returncode checking on `subprocess.run()` to catch binary execution errors.

Testing:
- No automated tests currently documented.
'''