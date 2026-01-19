import pygame, sys, time
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
    # "name": (baseHP, ((Name, healthMultiplier, Amount[-1 for infinite, -2 for boss (only 1)], startTime(startEvent(e.g. boss, hp, start), seconds), interval(low, higher)), (other units)), maxNumberOfEnemies, "background")
    "Korea": (1000, (("Doge", 150, 1, ("start", 0), (0, 0)), 
                     ("Doge", 150, -1, ("start", 20), (6, 10))
                    ),
                    3,
                    "Bg000.png"),
    "Cambodia": (1500, (("Doge", 150, -1, ("start", 0), (6, 10)), 
                        ("Snache", 150, -1, ("start", 0), (10, 26.67)), 
                        ("ThoseGuys", 150, -1, ("start", 0), (10, 26.67))
                        ),
                        6,
                        "Bg001.png"),
    "Singapore": (6000, (("Doge", 150, -1, ("start", 0), (4, 10)), 
                         ("Doge", 150, -1, ("start", 30), (6, 30)), 
                         ("Snache", 150, -1, ("start", 60), (10, 30)), 
                         ("ThoseGuys", 150, -1, ("start", 90), (10, 30)), 
                         ("ThoseGuys", 150, 20, ("hp", 60), (0.07, 0.13))
                        ),
                        10,
                        "Bg000.png"),
    "Dubai": (10000, (("Doge", 150, -1, ("start", 0), (6.67, 13.33)),
                      ("Snache", 150, -1, ("start", 20), (6.67, 13.33)),
                      ("ThoseGuys", 150, -1, ("start", 40), (6.67, 13.33)),
                      ("ThoseGuys", 150, 6, ("hp", 90), (2, 4)),
                      ("JackiePeng", 150, 1, ("hp", 90), (0, 0)),
                      ("ThoseGuys", 150, -1, ("hp", 88), (3.33 - 13.33)), 
                      ("JackiePeng", 150, 1, ("hp", 88), (0, 0)),
                    ), 
                    12,
                    "Bg005.png"),
    "South Africa": (14000, (("Doge", 150, -1, ("start", 0), (1, 10)),
                             ("Snache", 150, -1, ("start", 0), (1, 10)),
                             ("ThoseGuys", 150, -1, ("start", 0), (1, 10)),
                             ("JackiePeng", 150, 1, ("start", 100), (0, 0)),
                             ("JackiePeng", 150, 1, ("start", 102), (0, 0)),
                             ("Pigge", 150, -1, ("start", 133.33), (40, 60)),
                             ("Hippoe", 150, -1, ("start", 133.33), (40, 60)),
                             ("JackiePeng", 150, 2, ("hp", 20), (0.5, 1))
                             ),
                             10,
                             "Bg002.png"),
    "Turkey": (20000, (("Doge", 150, -1, ("start", 0), (1, 10)),
                       ("Snache", 150, -1, ("start", 0), (1, 10)),
                       ("ThoseGuys", 150, -1, ("start", 0), (1, 10)),
                       ("BaaBaa", 150, -1, ("start", 60), (60, 120)),
                       ("Pigge", 150, -1, ("start", 60), (60, 120)),
                       ("Hippoe", 150, -1, ("start", 80), (60, 120)),
                       ("Gorie", 150, -1, ("start", 133.33), (60, 120)),
                       ("JackiePeng", 150, -1, ("start", 80), (60, 120)),
                       ),
                       10,
                       "Bg002.png"),
    "Monaco": (30000, (("Doge", 150, -1, ("start", 0), (1, 10)),
                       ("Snache", 150, -1, ("start", 0), (1, 10)),
                       ("ThoseGuys", 150, -1, ("start", 20), (1, 2)),
                       ("Hippoe", 150, 1, ("start", 40), (0, 0)),
                       ("BaaBaa", 150, -1, ("hp", 50), (4.33, 8)),
                       ("JackiePeng", 150, -1, ("hp", 50), (4.33, 8)),
                       ),
                       5,
                       "Bg005.png"),
    "Denmark": (36000, (("Doge", 150, -1, ("start", 0), (3.33, 30)),
                        ("Snache", 150, -1, ("start", 10), (10, 20)),
                        ("ThoseGuys", 150, -1, ("start", 20), (10, 10)),
                        ("Croco", 150, -1, ("start", 40), (10, 40)),
                        ("LeBoin", 150, -2, ("hp", 90), 0),
                        ("ThoseGuys", 150, -1, ("hp", 90), (0.07, 1)),
                        ("ThoseGuys", 150, 20, ("hp", 90), (0.07, 0.07)),
                        ),
                        10,
                        "Bg000.png"),
    "Canada": (36000, (("Snache", 150, -1, ("start", 10), (5, 6.67)),
                       ("ThoseGuys", 150, -1, ("start", 20), (6.67, 10)),
                       ("Croco", 150, -1, ("start", 40), (10, 20)),
                       ("BaaBaa", 150, -1, ("start", 60), (10, 20)),
                       ("Gorie", 150, -1, ("start", 100), (30, 60)),
                       ("SirSeal", 150, -1, ("start", 200), (30, 60)),
                       ("JackiePeng", 150, -1, ("start", 80), (30, 60)),
                       ("Hippoe", 150, -1, ("start", 120), (30, 60)),
                       ("Pigge", 150, -1, ("start", 120), (30, 60)),
                       ("Gorie", 150, -1, ("start", 133.33), (30, 60)),
                       ("Gorie", 150, -1, ("hp", 50), (0.07, 0.07)),
                       ),
                       6,
                       "Bg000.png"),
    "Colombia": (40000, (("Doge", 150, -1, ("start", 0), (3.33, 10)),
                         ("Snache", 150, -1, ("start", 13.33), (3.33, 10)),
                         ("ThoseGuys", 150, -1, ("start", 6.67), (3.33, 10)),
                         ("Croco", 150, -1, ("start", 80), (3.33, 10)),
                         ("BBBunny", 150, -1, ("start", 100), (3.33, 13.33)),
                         ("BaaBaa", 150, -1, ("start", 100), (3.33, 20)),
                         ("Hippoe", 150, -1, ("start", 120), (30, 60)),
                         ("Pigge", 150, -1, ("start", 120), (30, 60)),
                         ("KangRoo", 150, 1, ("start", 100), (0, 0)),
                         ("KangRoo", 150, 1, ("start", 166.67), (0, 0)),
                         ),
                         4,
                         "Bg000.png"),
    "Easter Island": (40000, (("ThoseGuys", 150, -1, ("start", 0), (1, 10)),
                              ("Croco", 150, -1, ("start", 20), (10, 30)),
                              ("SquireRels", 150, -1, ("start", 0), (1, 16.67)),
                              ("OneHorn", 150, 1, ("start", 0), (0, 0)),
                              ("OneHorn", 150, -2, ("hp", 80), (0, 0)),
                              ),
                              10,
                              "Bg000.png"),
    "Hollywood": (40000, (("Hippoe", 150, -1, ("start", 0), (1, 2)),
                         ("Pigge", 150, -1, ("start", 0), (1, 2)),
                         ("JackiePeng", 150, -1, ("start", 40), (10, 20)),
                         ("Gorie", 150, -1, ("start", 60), (13.33, 30)),
                         ("SirSeal", 150, -1, ("start", 80), (40, 53.33)),
                         ("LeBoin", 150, -1, ("start", 100), (73.33, 113.33)),
                         ("KangRoo", 150, -1, ("start", 120), (43.33, 80)),
                         ("Mooth", 150, 1, ("start", 140), (0, 0)),
                         ),
                         2,
                         "Bg000.png"),
    "Moon": (200000, (("ThoseGuys", 150, -1, ("start", 0), (0.13, 1)),
                      ("Croco", 150, -1, ("start", 20), (0.27, 1.33)),
                      ("BBBunny", 150, -1, ("start", 20), (0.27, 1.33)),
                      ("KangRoo", 150, -1, ("start", 0), (13.33, 60)),
                      ("SirSeal", 150, -1, ("start", 0), (10, 40)),
                      ("Mooth", 150, -1, ("start", 40), (60, 80)),
                      ("Gorie", 150, -1, ("hp", 99), (6.67, 20)),
                      ("Pigge", 150, -1, ("hp", 99), (6.67, 20)),
                      ("ThoseGuys", 150, -1, ("hp", 99), (0.67, 2)),
                      ("Mooth", 150, 4, ("hp", 99), (0.07, 0.07)),
                      ("KangRoo", 150, 6, ("hp", 99), (0.07, 4)),
                      ("SirSeal", 150, 6, ("hp", 99), (4, 13.33)),
                      ("Gorie", 150, 10, ("hp", 99), (0.07, 1.33)),
                      ("BunBun", 150, -2, ("hp", 70), (0, 0)),
                      ),
                      8,
                      "Bg006.png")
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
# name, level, cooldown timer
hotbar = [["NONE", 1, 0], ["NONE", 1, 0], ["NONE", 1, 0], ["NONE", 1, 0], ["NONE", 1, 0], ["NONE", 1, 0], ["NONE", 1, 0], ["NONE", 1, 0], ["NONE", 1, 0], ["NONE", 1, 0]]

# side = "cat" or "enemy", name = unit's name, level
def deploy(side, name, level):
    # hotbar slot time is current time - cooldown = => then can depoly
    deploySound.play()
    # set hotbar list index thingy to current time
    print(f"{side};{name};{level}")

def menuNav(direction):
    # for arrows
    print(f"menuNav: {direction}")

workerCatLevel = 0
def upgradeWorkerCat():
    print("upgrade worker cat")

currentStage = "Korea"
inStage = True
currentMoney = 0
currentEnemies = [] # times for finding intervals
currentOpponentBaseHp= 0
currentBaseHp = 0
def playStage(currentStage):
    for i in range(stages[currentStage][1].length):
        currentEnemies.append([])
    currentMoney = 0
    richCatLevel = 0
    currentOpponentBaseHp = stages[currentStage][0]
    stageStartTime = time.time()
    enterBattleSound.play()

    while inStage:
        for i in range(currentEnemies):
            if int(time.time() - stageStartTime) in currentEnemies:
                print()



# =================================
# MAIN LOOP
# =================================
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
                        upgradeWorkerCat()
                    case _:
                        blockSound.play()
            if not inStage:
                print()
                
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