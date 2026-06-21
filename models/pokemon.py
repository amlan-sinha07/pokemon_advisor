from models.move import Move

class Pokemon:
    def __init__(self,name:str,types:list,moves:list,stats: dict,max_hp:int=100):
        self.name=name
        self.types=types
        self.stats=stats
        self.moves=moves
        self.max_hp=max_hp
        self.current_hp=stats["hp"]


    def is_alive(self)->bool:
        return self.current_hp>0
    def learn_move(self,move:Move):
        #adds a move to the move pool , respecting the 4-move limit
        if len(self.moves) >=4:
            print(f"{self.name} already knows 4 moves! Forget a move first.")
            return False
        self.moves.append(move)
        return True
    def heal(self,amount:int):
        self.current_hp=min(self.stats["hp"],self.current_hp+amount)
    def get_types(self)->list:
        return self.types
    
    def take_damage(self, damage: int):
        self.current_hp = max(0, self.current_hp - damage)
        print(f"{self.name} took {damage} damage! "
              f"HP: {self.current_hp}/{self.stats['hp']}")
        
       
    def __str__(self):
        return (f"{self.name}"
                f"[{'/'.join(self.types)}]"
                f"HP: {self.current_hp}/{self.stats['hp']}")