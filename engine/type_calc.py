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
            self.chart=json.load(f)
    def effectiveness(self,attacking_type:str,defending_type:str)->float:
        attack=attacking_type.strip().lower()
        defend=defending_type.strip().lower()

        matching_attack_key =None
        for key in self.chart.keys():
            if key.lower() == attack:
                matching_attack_key =key
                break
        if matching_attack_key is None:
            raise ValueError(f"unknown type: {attacking_type}")
        inner_chart = self.chart[matching_attack_key]

        for key , value in inner_chart.items():
            if key.lower() == defend:
                return float(value)
        return 1.0
        #if attacking_type not in self.chart:
        #    raise ValueError(f"unknown type:{attacking_type}")
        #return self.chart[attacking_type].get(defending_type,1.0)
    def dual_type_effectiveness(self,attacking_type:str,defend_type1:str,defend_type2:str=None)->float:
        e1=self.effectiveness(attacking_type,defend_type1)
        #if there is no second type then just return first effectiveness
        if defend_type2 is None or defend_type2=="":
            return e1
        
        e2=self.effectiveness(attacking_type,defend_type2)
        return e1*e2
'''
Module: type_calc.py

Responsibilities:
- Calculates type effectiveness multipliers for single and dual-type Pokémon matchups.
- Loads and manages the Pokémon type interaction matrix from local JSON configuration.

Dependencies:
- standard -> json, os

Known problems:
- Inefficient $O(N)$ lookup: Iterates through all dictionary keys on every call to `effectiveness` to perform case-insensitive matching, rather than normalizing keys once at initialization.
- Missing error handling for file I/O: `__init__` lacks exception handling if `type_chart.json` is missing or corrupted.

Testing:
- No automated tests currently documented.
'''