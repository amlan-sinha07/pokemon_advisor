import math
import subprocess
from pathlib import Path

from models.pokemon import Pokemon
from models.move import Move
from engine.type_calc import TypeCalculator

class DamageCalculator:
    def __init__(self):
        self.type_calc=TypeCalculator()
        self.cpp_calc=(
            Path(__file__).resolve().parent / "damage_calc.exe"
        )
    def calculate_cpp(
            self,
            power:int,
            atk:int,
            def_stat:int,
            effectiveness:float,
            stab:float
        )->int | None:
        if not self.cpp_calc.is_file():
            return None
        input_str = (
            f"{power} {atk} {def_stat} "
            f"{effectiveness} {stab}\n"
        )
        try:
            result=subprocess.run(
                [str(self.cpp_calc)],
                input=input_str,
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )
        except (OSError,subprocess.TimeoutExpired) as exc:
            print(f"C++ engine execution failed: {exc}")
            return None
        if result.returncode != 0:
            print(
                f"C++ engine error: {result.stderr.strip()}"
            )
            return None
        try:
            damage=int(result.stdout.strip())
        except ValueError:
            print("C++ engine returned invalid output.")
            return None
        if damage<0:
            print("C++ engine returned negative output.")
            return None
        return damage
    def calculate(
            self,
            attacker:Pokemon,
            defender:Pokemon,
            move:Move
        )->dict:
        if not move.is_damaging():
            return {
                "damage":0,
                "effectiveness":1.0,
                "note":"status move"
            }
        stab=(
            1.5 if move.move_type in attacker.types else 1.0
        )
        effectiveness=1.0
        for defend_type in defender.types:
            effectiveness *= self.type_calc.effectiveness(
                move.move_type,
                defend_type
            )
        if move.category=="Physical":
            atk=attacker.stats["atk"]
            defense=defender.stats["def"]
        else:
            atk=attacker.stats["spa"]
            defense=defender.stats["spd"]
        if defense <= 0:
            raise ValueError(
                "Defender's defensive stat must be perspective."
            )
        cpp_result = self.calculate_cpp(
            move.power,
            atk ,
            defense,
            effectiveness,
            stab
        )
        if cpp_result is not None:
            damage = cpp_result
            engine= "C++"
        else:
            base = (
                ((2*50/5+2)* move.power*atk/defense)/50
            ) + 2
            damage= math.floor(
                base * stab *effectiveness + 0.5
            )
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
Keep with cleanup	Fix documentation and validation-message typo
Known problems:

Testing:
- tests/test_damage_calc.py.
'''