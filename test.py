import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Animation')

WHITE = (255, 255, 255)
catImgs = []
for i in range(17):    
    catImgs.append(pygame.image.load(f'Cats/Cat/Normal/Walk/frame_{i}.png'))
catx = 1000
caty = 500
direction = 'right'
frame = 0
running = True
while running: # the main game loop
    DISPLAYSURF.fill(WHITE)

    DISPLAYSURF.blit(catImgs[frame], (catx, caty))
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