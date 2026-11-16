"""
Module: move.py

Responsibilities:
- Represents a Pokemon move.
- Stores move attributes.
- Determines whether a move deals direct damage.

Dependencies:
- None

Testing:
- Covered by tests/test_move.py.
"""
class Move:
    def __init__(self,name:str,move_type:str,
                 power:int,category:str,accuracy:int):
        self.name=name
        self.move_type=move_type
        self.power=power
        self.category=category
        self.accuracy=accuracy
    def is_damaging(self)->bool:
        return self.category !="Status" and self.power>0
    def __str__(self):
        return (f"{self.name}   "
                f"[{self.move_type}]    "
                f"Power:{self.power}    "
                f"Cat:{self.category}   "
                f"Acc:{self.accuracy}   ")