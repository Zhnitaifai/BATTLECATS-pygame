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
            self.xHitbox = self.x+200 if self.name != "CatBase" else 10
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
                self.walkAnimations.append(pygame.transform.scale(animation, ((170, 700) if self.stats[3] == 0 else ((500, 350) if self.name != "BunBun" else (750, 500)))))
            self.attackAnimations = []
            for i in range(self.stats[8]):    
                animation = pygame.image.load(f'Enemies/{name}/Attack/frame_{i}.png')
                self.attackAnimations.append(pygame.transform.scale(animation, ((500, 350) if self.name != "BunBun" else (750, 500))))
            self.currentFrame = 0
            self.currentAnimation = 0
            self.x = 0 if self.stats[3] != 0 else 100
            self.y = 0 if self.stats[3] == 0 else random.randint(*((400, 450) if self.name != "BunBun" else (200, 250)))
            self.xHitbox = self.x+200
            #(-100 if self.stats[3] == 0 else 200)
            
    def unitUpdate(self, positions):
        attack = False
        targets = []
        antiRed = False
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
                    targets, antiRed = self.unitTargetUpdate(positions, self.stats[9])
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
        self.xHitbox = self.x+((200 if self.name != "CatBase" else 10) if self.type == 'cat' else (300 if self.stats[3] != 0 else 100))
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
            "hitbox": (self.xHitbox, self.y + (400 if self.stats[3] == 0 else 0)), 
            "attack?": attack, 
            "damage": self.attack, 
            "targets": (targets, antiRed)
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
        antiRed = True if self.name in ["Axe", "Fish"] else False
        if self.type == 'cat':
            detectBox = Rect(self.xHitbox-self.stats[2], self.y-400, self.stats[2], 1000)    
        else:
            detectBox = Rect(self.xHitbox, self.y-600, self.stats[2], 1000)  
        for i in positions:
            if detectBox.collidepoint(positions[i][0], positions[i][1]):
                targets.append(i)
                if attackType == 0:
                    return targets, antiRed
        return targets, antiRed
    
    def takeDamage(self, damage, antired):
        red = False if self.name not in ["BBBunny", "OneHorn", "Pigge"] else True
        self.health -= damage*(2 if red and antired else 1)
        if self.knockbackCount != 0:
            if self.health < self.stats[0]/self.knockback*self.knockbackCount:
                self.state = 'knockback'
                self.knockbackCount -= 1
                self.knockbackFrame = 24
        if self.health <= 0:
            return True
        return False
            
            
    def getHealth(self):
        return self.health

    def getMoney(self):
        return self.stats[0] + self.attack