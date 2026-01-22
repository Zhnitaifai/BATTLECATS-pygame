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
        self.attackState = 'foreswing'
        self.name = name
        self.attackCooldown = 0
        self.level = int(level)
        self.knockbackFrame = 0

        if type == 'cat':
            self.stats = open(f'Cats/{name}/stats.csv')
            self.stats = self.stats.readline().split(",")
            for i in range(len(self.stats)):
                self.stats[i] = int(self.stats[i]) 
            self.health = int(self.stats[0]*(1+(self.level-1)*.2))
            self.attack = int(self.stats[1]*(1+(self.level-1)*.2))
            self.knockback = self.stats[6]
            self.knockbackCount = self.stats[6]-1
            self.walkAnimations = []
            for i in range(self.stats[7]):    
                animation = pygame.image.load(f'Cats/{name}/{'Normal' if self.level < 10 else 'Evolved'}/Walk/frame_{i}.png')
                self.walkAnimations.append(pygame.transform.scale(animation, (170, 600) if self.name == 'CatBase' else ((500, 350) if self.name != "Baha" else (750, 500))))
            self.attackAnimations = []
            # 26 if self.name == "Bird" and self.level >= 10 else 
            for i in range(26 if self.name == "Bird" and self.level >= 10 else self.stats[8]):    
                animation = pygame.image.load(f'Cats/{name}/{'Normal' if self.level < 10 else 'Evolved'}/Attack/frame_{i}.png')
                self.attackAnimations.append(pygame.transform.scale(animation, ((500, 350) if self.name != "Baha" else (750, 500))))
            self.currentFrame = 0
            self.x = 1400 if self.name != "CatBase" else 1600
            self.y = 100 if self.name == "CatBase" else random.randint(*((400, 450) if self.name != "Baha" else (200, 250)))
            self.xHitbox = self.x+200
        elif type == 'enemy':
            self.stats = open(f'Enemies/{name}/stats.csv')
            self.stats = self.stats.readline().split(",")
            for i in range(len(self.stats)):
                self.stats[i] = int(self.stats[i]) 
            self.health = int(self.stats[0]*self.level/100)
            self.attack = int(self.stats[1]*self.level/100)
            self.knockback = self.stats[6]
            self.knockbackCount = self.stats[6]-1
            self.walkAnimations = []
            for i in range(self.stats[7]):    
                animation = pygame.image.load(f'Enemies/{name}/Walk/frame_{i}.png')
                self.walkAnimations.append(pygame.transform.scale(animation, ((500, 350) if self.name != "BunBun" else (750, 500))))
            self.attackAnimations = []
            for i in range(self.stats[8]):    
                animation = pygame.image.load(f'Enemies/{name}/Attack/frame_{i}.png')
                self.attackAnimations.append(pygame.transform.scale(animation, ((500, 350) if self.name != "BunBun" else (750, 500))))
            self.currentFrame = 0
            self.currentAnimation = 0
            self.x = 200
            self.y = random.randint(*((400, 450) if self.name != "BunBun" else (200, 250)))
            self.xHitbox = self.x+200
            
    def unitUpdate(self, positions):
        attack = False
        targets = []
        self.attackCooldown -= (1 if self.attackCooldown > 0 else 0)
        if self.state == 'walk':
            self.currentFrame += 1
            if self.currentFrame >= len(self.walkAnimations):
                self.currentFrame = 0
            self.currentAnimation = self.walkAnimations[self.currentFrame]
            if self.type == 'cat':
                self.x -= int(self.stats[3]/2)
            else:
                self.x += int(self.stats[3]/2)
        elif self.state == 'attack':
            print(self.currentFrame)
            print(len(self.attackAnimations))
            match self.attackState:
                case "foreswing":
                    self.currentFrame += 1
                    self.currentAnimation = self.attackAnimations[self.currentFrame]
                    if self.currentFrame == self.stats[4]:
                        self.attackState = "damage"
                case "damage":
                    self.currentFrame += 1
                    self.currentAnimation = self.attackAnimations[self.currentFrame]
                    self.attackState = "backswing"
                    self.attackCooldown = self.stats[5]
                    attack = True
                    targets = self.unitTargetUpdate(positions, self.stats[9])
                case "backswing":
                    self.currentFrame += 1
                    if self.currentFrame >= len(self.attackAnimations):
                        self.currentFrame = 0
                        self.currentAnimation = self.walkAnimations[self.currentFrame]
                        self.attackState = "foreswing"
                        self.state = "walk"
                    else:
                        self.currentAnimation = self.attackAnimations[self.currentFrame]
        elif self.state == 'idle':
            self.currentAnimation = self.walkAnimations[0]
            if self.attackCooldown == 0:
                self.state = "walk"
        self.xHitbox = self.x+(200 if self.type == 'cat' else 300)
        if self.state == 'knockback':
            if self.knockbackFrame != 0:
                self.x -= (-15 if self.type == 'cat' else 15)
                self.currentAnimation = pygame.transform.rotate(self.attackAnimations[0], (-45 if self.type == 'cat' else 45))
                self.xHitbox = 0
                self.knockbackFrame -= 1
            else:
                self.state = 'walk'
        return {
            "animation": self.currentAnimation, 
            "displayPos": (self.x, self.y - (150 if self.state == 'knockback' else 0)), 
            "hitbox": (self.xHitbox, self.y), 
            "attack?": attack, 
            "damage": self.attack, 
            "targets": targets
        }
    
    def unitDetectionUpdate(self, positions):
        if self.type == 'cat':
            detectBox = Rect(self.xHitbox-self.stats[2], self.y-400, self.stats[2], 1000)    
        else:
            detectBox = Rect(self.xHitbox, self.y-400, self.stats[2], 1000)  
        for i in positions:
            if detectBox.collidepoint(positions[i][0], positions[i][1]) and self.state not in ['attack', 'knockback']:
                self.state = ('attack' if self.attackCooldown == 0 else "idle")
                self.currentFrame = 0
                
                return True, detectBox
            elif self.state == 'idle':
                self.state = 'walk'
        return False, detectBox
    
    def unitTargetUpdate(self, positions, attackType):
        targets = []
        if self.type == 'cat':
            detectBox = Rect(self.xHitbox-self.stats[2], self.y-400, self.stats[2], 1000)    
        else:
            detectBox = Rect(self.xHitbox, self.y-600, self.stats[2], 1000)  
        for i in positions:
            if detectBox.collidepoint(positions[i][0], positions[i][1]):
                targets.append(i)
                if attackType == 0:
                    return targets
        return targets
    
    def takeDamage(self, damage):
        self.health -= damage
        if self.knockbackCount != 0:
            if self.health < self.stats[0]/self.knockback*self.knockbackCount:
                self.state = 'knockback'
                self.knockbackCount -= 1
                self.knockbackFrame = 24
        if self.health <= 0:
            return True
        return False
            
            
            