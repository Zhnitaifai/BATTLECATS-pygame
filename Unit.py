from enum import Enum, auto
class State(Enum):
    IDLE = auto()
    WALKING = auto()
    ATTACKING = auto()
    KNOCKED_BACK = auto()
    
class Unit:
    def __init__(self, type, name, level):
        
        if type == 'cat':
            stats = open(f'Cats/{name}/stats.csv').split(",")
            health = stats[0]*(1+(level-1)*.2)
            
            