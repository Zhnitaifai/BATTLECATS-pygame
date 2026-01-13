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
catDict = []
enemyDict = []
catAmt = 0
enemyAmt = 0
def deploy(type, name, level):
    new_unit = Unit(type, name, level)
    if type == 'cat':
        catDict.update({f'{name}{catAmt+1}': new_unit})
        catAmt += 1
while running: # the main game loop
    DISPLAYSURF.blit(bg, (0, -420))

    catPos = {}
    enemyPos = {}
    catDisplay = {}
    enemyDisplay = {}
    if len(catDict) > 0:
        for i in (catDict):
            display = catDict[i].unitUpdate()
            catPos.update({i: display[2]})
            catDisplay.update({i: display[1]})
    if len(enemyDict) > 0:
        for i in (enemyDict):
            display = enemyDict[i].unitUpdate()
            enemyPos.update({i: display[2]})
            enemyDisplay.update({i: display[1]})
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
            elif event.key == pygame.K_1:
                deploy("cat", "Cat", "1")

    pygame.display.update()
    fpsClock.tick(FPS)
    
pygame.quit()