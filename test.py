import pygame, sys
from pygame.locals import *
import Unit
from Unit import *
pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Animation')

WHITE = (255, 255, 255)
catImgs = []
for i in range(17):  
    animation = pygame.image.load(f'Cats/Cat/Normal/Walk/frame_{i}.png')
    catImgs.append(pygame.transform.scale(animation, (500, 350)))
bg = pygame.transform.scale(pygame.image.load('backgrounds/classicBG.png'), (2000, 1500))
catx = 1300
caty = 500
direction = 'right'
frame = 0
running = True
catDict = {}
enemyDict = {}
catAmt = 0
enemyAmt = 0

def deploy(type, name, level, Amt):
    new_unit = Unit(type, name, level)
    if type == 'cat':
        catDict.update({f'{name}{catAmt+1}': new_unit})
        
    else: 
        enemyDict.update({f'{name}{enemyAmt+1}': new_unit})
        
catPos = {}
enemyPos = {}
while running: # the main game loop
    DISPLAYSURF.blit(bg, (0, -420))
    catPos = {}
    if len(catDict) > 0:
        for i in (catDict):
            display = catDict[i].unitUpdate(enemyPos)
            catPos.update({i: display[2]})
            DISPLAYSURF.blit(display[0], display[1])
            catDict[i].unitDetectionUpdate(enemyPos)
            if display[3]:
                for i in display[5]:
                    enemyDict[i].takeDamage(display[4])
    enemyPos = {}
    if len(enemyDict) > 0:
        for i in (enemyDict):
            display = enemyDict[i].unitUpdate(catPos)
            enemyPos.update({i: display[2]})
            DISPLAYSURF.blit(display[0], display[1])
            enemyDict[i].unitDetectionUpdate(catPos)
    if len(catDict) > 0:
        for i in (catDict):
            catDict[i].unitDetectionUpdate(enemyPos)
    if len(enemyDict) > 0:
        for i in (enemyDict):
            enemyDict[i].unitDetectionUpdate(catPos)
    frame += 1
    if frame > 16:
        frame = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_0:
                deploy("cat", "Cat", "1", catAmt)
                catAmt += 1
            elif event.key == pygame.K_1:
                deploy("notCat", "Doge", "100", enemyAmt)
                enemyAmt += 1

    pygame.display.update()
    fpsClock.tick(FPS)
    
pygame.quit()