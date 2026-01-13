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
    - MENU
        - instructions if 1st time
        - start button
        - upgrade cats
        - 
    - STAGE
        - start level from start
    - PAUSE
        - pauses menu, only during play state
    - RESUME
        - unpauses
    - END
        - end screen (Rewards)
'''
# stats for all stages
stages = {
    # "name": (baseHP, ((Name, Amount[-1 for infinite], startTime[seconds], interval(low, higher))), maxNumberOfEnemies)
    "Korea": (1000, (("Doge", 1, 0, 0), ("Doge", -1, 20, (6, 10))), 3)
}

# def playAudio(name):
attackSound = pygame.mixer.Sound('Music/bcAttack.ogg')
attackBaseSound = pygame.mixer.Sound('Music/bcAttackBase.ogg')
blockSound = pygame.mixer.Sound('Music/bcBlock.ogg')
bossShockwaveSound = pygame.mixer.Sound('Music/bcBossShockwave.ogg')
clickSound = pygame.mixer.Sound('Music/bcClick.ogg')
defeatSound = pygame.mixer.Sound('Music/bcDefeat.ogg')
deploySound = pygame.mixer.Sound('Music/bcDeploy.ogg')
enterBattleSound = pygame.mixer.Sound('Music/bcEnterBattle.ogg')
rewardSound = pygame.mixer.Sound('Music/bcReward.ogg')
scrollingSound = pygame.mixer.Sound('Music/bcScrolling.ogg')
unitDiesSound = pygame.mixer.Sound('Music/bcUnitDies.ogg')
unitRecharged = pygame.mixer.Sound('Music/bcUnitRecharge.ogg')
victory = pygame.mixer.Sound('Music/bcVictory.ogg')

# pygame.mixer.music.play(-1, 0.0) #-1: play forever, 0.0 = starting point
backgroundMusicPlaying = True

# Controls
hotBarSwitch = 1 #1st row = 1, 2nd row = 2
keyPressedBoolean = [
    ["q", False],
    ["w", False],
    ["e", False],
    ["r", False],
    ["t", False],
    ["a", False],
    ["s", False],
    ["d", False],
    ["f", False],
    ["g", False],
    ["enter", False],
    ["uarrow", False],
    ["darrow", False],
    ["larrow", False],
    ["rarrow", False],
    ["tab", False],
]

# list of cats on hotbar going into battle
# name, level
hotbar = [["NONE", 1], ["NONE", 1], ["NONE", 1], ["NONE", 1], ["NONE", 1], ["NONE", 1], ["NONE", 1], ["NONE", 1], ["NONE", 1], ["NONE", 1]]

# side = "cat" or "enemy", name = unit's name, level
def deploy(side, name, level):
    deploySound.play()
    print(f"{side};{name};{level}")

def menuNav(direction):
    # for arrows
    print(f"menuNav: {direction}")

richCatLevel = 0
def upgradeRichCat():
    print("upgrade rich cat")

while True:
    screen.fill("red")
    pygame.display.update()

    # key press detection
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # QWERT
            # ASDFG
            # general navigation w/ enter & arrow keys
            if event.key == K_q:
                keyPressedBoolean[0] = True
            if event.key == K_w:
                keyPressedBoolean[1] = True
            if event.key == K_e:
                keyPressedBoolean[2] = True
            if event.key == K_r:
                keyPressedBoolean[3] = True
            if event.key == K_t:
                keyPressedBoolean[4] = True
            if event.key == K_a:
                keyPressedBoolean[5] = True
            if event.key == K_s:
                keyPressedBoolean[6] = True
            if event.key == K_d:
                keyPressedBoolean[7] = True
            if event.key == K_f:
                keyPressedBoolean[8] = True
            if event.key == K_g:
                keyPressedBoolean[9] = True
            if event.key == K_RETURN:
                keyPressedBoolean[10] = True
            if event.key == K_UP:
                keyPressedBoolean[11] = True
            if event.key == K_DOWN:
                keyPressedBoolean[12] = True
            if event.key == K_LEFT:
                keyPressedBoolean[13] = True
            if event.key == K_RIGHT:
                keyPressedBoolean[14] = True
            if event.key == K_TAB:
                keyPressedBoolean[15] = True
        if event.type == KEYUP:
            # for resetting
            if event.key == K_q:
                keyPressedBoolean[0] = False
            if event.key == K_w:
                keyPressedBoolean[1] = False
            if event.key == K_e:
                keyPressedBoolean[2] = False
            if event.key == K_r:
                keyPressedBoolean[3] = False
            if event.key == K_t:
                keyPressedBoolean[4] = False
            if event.key == K_a:
                keyPressedBoolean[5] = False
            if event.key == K_s:
                keyPressedBoolean[6] = False
            if event.key == K_d:
                keyPressedBoolean[7] = False
            if event.key == K_f:
                keyPressedBoolean[8] = False
            if event.key == K_g:
                keyPressedBoolean[9] = False
            if event.key == K_RETURN:
                keyPressedBoolean[10] = False
            if event.key == K_UP:
                keyPressedBoolean[11] = False
            if event.key == K_DOWN:
                keyPressedBoolean[12] = False
            if event.key == K_LEFT:
                keyPressedBoolean[13] = False
            if event.key == K_RIGHT:
                keyPressedBoolean[14] = False
            if event.key == K_TAB:
                keyPressedBoolean[15] = False
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

    currentKeyPresses = list(filter(lambda value: value, keyPressedBoolean))
    print(currentKeyPresses)
    match GAMESTATE:
        case "STAGE":
            for every in currentKeyPresses:
                match every[0]:
                    case "q":
                        deploy("cat", hotbar[0][0], hotbar[0][1])
                    case "w":
                        deploy("cat", hotbar[1][0], hotbar[1][1])
                    case "e":
                        deploy("cat", hotbar[2][0], hotbar[2][1])
                    case "r":
                        deploy("cat", hotbar[3][0], hotbar[3][1])
                    case "t":
                        deploy("cat", hotbar[4][0], hotbar[4][1])
                    case "a":
                        deploy("cat", hotbar[5][0], hotbar[5][1])
                    case "s":
                        deploy("cat", hotbar[6][0], hotbar[6][1])
                    case "d":
                        deploy("cat", hotbar[7][0], hotbar[7][1])
                    case "f":
                        deploy("cat", hotbar[8][0], hotbar[8][1])
                    case "g":
                        deploy("cat", hotbar[9][0], hotbar[9][1])
                    case "tab":
                        upgradeRichCat()
                    case _:
                        blockSound.play()
        case _:
            for every in currentKeyPresses:
                match every[0]:
                    case "":
                        print()
        
    # start screen -> go directly to cat base screen
        # only have START, UPGRADE, xp bar (top right)
    #     # If doing gacha add catfood, rare cat capcule button

    # Gameplay

    # end screen

    pygame.display.update()
    fpsClock.tick(fps)