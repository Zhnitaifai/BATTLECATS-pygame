from enum import Enum, auto
import pygame
from pygame.locals import *
import random
class State(Enum):
    IDLE = auto()
    WALKING = auto()
    ATTACKING = auto()
    KNOCKED_BACK = auto()
    
class Unit:
    def __init__(self, type, name, level):
        
        if type == 'cat':
            self.stats = open(f'Cats/{name}/stats.csv')
            self.stats = self.stats.readline().split(",")
            self.health = self.stats[0]*(1+(level-1)*.2)
            self.walkAnimations = []
            for i in range(self.stats[7]):    
                animation = pygame.image.load(f'Cats/Cat/Normal/Walk/frame_{i}.png')
                self.walkAnimations.append(pygame.transform.scale(animation(500, 350)))
            self.currentAnimation = 0
            self.x = 1300
            self.y = random.randint(500, 600)
            
    def unitUpdate(self):
        self.currentAnimation += 1
        self.x -= self.stats[3]
        return self.walkAnimations[self.currentAnimation], (self.x, self.y)
            
            
            