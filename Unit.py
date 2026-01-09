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
        self.type = type
        self.state = 'walk'
        self.name = name
        if type == 'cat':
            self.stats = open(f'Cats/{name}/stats.csv')
            self.stats = self.stats.readline().split(",")
            for i in range(len(self.stats)):
                self.stats[i] = int(self.stats[i]) 
            self.health = self.stats[0]*(1+int(level-1)*.2)
            self.walkAnimations = []
            for i in range(self.stats[7]):    
                animation = pygame.image.load(f'Cats/{name}/Normal/Walk/frame_{i}.png')
                self.walkAnimations.append(pygame.transform.scale(animation, (500, 350)))
            self.currentAnimation = 0
            self.x = 1300
            self.y = random.randint(400, 450)
        elif type == 'notCat':
            self.stats = open(f'Enemies/{name}/stats.csv')
            self.stats = self.stats.readline().split(",")
            for i in range(len(self.stats)):
                self.stats[i] = int(self.stats[i]) 
            self.health = self.stats[0]*(1+int(level-1)*.2)
            self.walkAnimations = []
            for i in range(self.stats[7]):    
                animation = pygame.image.load(f'Enemies/{name}/Walk/frame_{i}.png')
                self.walkAnimations.append(pygame.transform.scale(animation, (500, 350)))
            self.currentAnimation = 0
            self.x = 200
            self.y = random.randint(400, 450)
            
    def unitWalkUpdate(self):
        if self.state == 'walk':
            self.currentAnimation += 1
            if self.currentAnimation >= len(self.walkAnimations):
                self.currentAnimation = 0
            if self.type == 'cat':
                self.x -= int(self.stats[3]/2)
            else:
                self.x += int(self.stats[3]/2)
        print(self.name, self.x, self.y)
        return self.walkAnimations[self.currentAnimation], (self.x, self.y)
    
    def unitDetectionUpdate(self, positions):
        if self.type == 'cat':
            detectBox = Rect(self.x, self.y+100, self.stats[2], 300)    
        else:
            detectBox = Rect(self.x, self.y+100, self.stats[2], 300)
        for i in positions:
            if detectBox.collidepoint(positions[i][1], positions[i][1]):
                self.state = 'attack'
                return True
        return False
            
            
            