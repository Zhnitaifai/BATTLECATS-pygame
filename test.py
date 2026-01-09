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
cat = Unit("cat", "Cat", 1)
tank = Unit("cat", "Tank", 1)
doge = Unit("notCat", "Doge", 1)
while running: # the main game loop
    DISPLAYSURF.blit(bg, (0, -420))

    catPos = {}
    enemiesPos = {}
    display = cat.unitWalkUpdate()
    catPos.update({"cat": display[1]})
    displau = tank.unitWalkUpdate()
    catPos.update({"tank": display[1]})
    displai = doge.unitWalkUpdate()
    enemiesPos.update({"doge": display[1]})
    cat.unitDetectionUpdate(enemiesPos)
    tank.unitDetectionUpdate(enemiesPos)
    doge.unitDetectionUpdate(enemiesPos)
    DISPLAYSURF.blit(display[0], display[1])
    DISPLAYSURF.blit(displau[0], displau[1])
    DISPLAYSURF.blit(displai[0], displai[1])
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

    pygame.display.update()
    fpsClock.tick(FPS)
    
pygame.quit()