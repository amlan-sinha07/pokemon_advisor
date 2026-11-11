#
#
#Typecalculator
import json
import os
class TypeCalculator:
    def __init__(self):
        # 18types of pokemon champions
        #
        #
        chart_path=os.path.join(
            os.path.dirname(__file__),
            "..","data","type_chart.json"
        )
        with open(chart_path,"r") as f:
            raw_chart=json.load(f)
            self.chart={
                attack.lower():{
                    defend.lower():float(multiplier)
                    for defend,multiplier in matchups.items()
                }
                for attack,matchups in raw_chart.items()
            }
    def effectiveness(
            self,
            attacking_type:str,
            defending_type:str
        )->float:
        attack=attacking_type.strip().lower()
        defend=defending_type.strip().lower()
        if attack not in self.chart:
            raise ValueError(
                f"Unknown type: {attacking_type}"
            )
        return self.chart[attack].get(defend,1.0)
    def dual_type_effectiveness(self,attacking_type:str,defend_type1:str,defend_type2:str=None)->float:
        e1=self.effectiveness(attacking_type,defend_type1)
        #if there is no second type then just return first effectiveness
        if defend_type2 is None or defend_type2=="":
            return e1
        
        e2=self.effectiveness(attacking_type,defend_type2)
        return e1*e2
"""
Module: type_calc.py

Responsibilities:
- Calculate single-type effectiveness.
- Calculate dual-type effectiveness.
- Load and normalize the Pokémon type chart.

Dependencies:
- json
- os

Testing:
- Covered by tests/test_type_calc.py.
"""