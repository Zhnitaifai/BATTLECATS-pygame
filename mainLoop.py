import pygame, sys
from pygame.locals import *

pygame.init()

fps = 30
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('BATTLE CATS')

GAMESTATE = "START"
'''
    GAME STATES:
    - START
        - start button
    - PLAY
        - start level from start
    - PAUSE
        - pauses menu, only during play state
    - RESUME
        - unpauses
    - END
        - end screen (Rewards)
'''

hotBarSwitch = 1 #1st row = 1, 2nd row = 2

keyPressed = {
    "q": False,
    "w": False,
    "e": False,
    "r": False,
    "t": False,
    "a": False,
    "s": False,
    "d": False,
    "f": False,
    "g": False,
    "enter": False
}

while True:
    screen.fill("red")
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # QWERT
            # ASDFG
            # general navigation w/ enter & arrow keys
            if event.key == K_q:
                keyPressed["q"] = True
            if event.key == K_w:
                keyPressed["w"] = True
            if event.key == K_e:
                keyPressed["e"] = True
            if event.key == K_r:
                keyPressed["r"] = True
            if event.key == K_t:
                keyPressed["t"] = True
            if event.key == K_a:
                keyPressed["a"] = True
            if event.key == K_s:
                keyPressed["s"] = True
            if event.key == K_d:
                keyPressed["d"] = True
            if event.key == K_f:
                keyPressed["f"] = True
            if event.key == K_g:
                keyPressed["g"] = True
        if event.type == KEYUP:
            # for resetting
            if event.key == K_q:
                keyPressed["q"] = False
            if event.key == K_w:
                keyPressed["w"] = False
            if event.key == K_e:
                keyPressed["e"] = False
            if event.key == K_r:
                keyPressed["r"] = False
            if event.key == K_t:
                keyPressed["t"] = False
            if event.key == K_a:
                keyPressed["a"] = False
            if event.key == K_s:
                keyPressed["s"] = False
            if event.key == K_d:
                keyPressed["d"] = False
            if event.key == K_f:
                keyPressed["f"] = False
            if event.key == K_g:
                keyPressed["g"] = False
            # for exitting program /w keyboard shortcut
            if event.key == K_ESCAPE:
                if GAMESTATE == "PAUSE":
                    GAMESTATE = "RESUME"
                else:
                    GAMESTATE = "PAUSE"
                print(GAMESTATE)
            if event.key == K_F4:
                pygame.quit()   
                sys.exit()
    # load screen for loading music?? might not be necessary
    
    # start screen -> go directly to cat base screen
        # only have START, UPGRADE, xp bar (top right)
        # If doing gacha add catfood, rare cat capcule button
    
    # Gameplay

    # end screen

    pygame.display.update()
    fpsClock.tick(fps)