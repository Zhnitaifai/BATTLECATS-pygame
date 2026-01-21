import pygame, sys, time
from pygame.locals import *
import Unit
import time

pygame.init()

fps = 30
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('BATTLE CATS')

GAMESTATE = "STAGE"
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
    - END
        - end screen (Rewards)
'''
# stats for all stages
stages = {
    # "name": (baseHP, ((Name, healthMultiplier, Amount[-1 for infinite, -2 for boss (only 1)], startTime(startEvent(e.g. boss, hp, start), seconds), interval(low, higher)), (other units)), maxNumberOfEnemies, "background", catLevel)
    "Korea": (1000, (("Doge", 150, 1, ("start", 0), (0, 0)), 
                     ("Doge", 150, -1, ("start", 20), (6, 10))
                    ),
                    3,
                    "Bg000.png", 
                    1),
    "Cambodia": (1500, (("Doge", 150, -1, ("start", 0), (6, 10)), 
                        ("Snache", 150, -1, ("start", 0), (10, 26.67)), 
                        ("ThoseGuys", 150, -1, ("start", 0), (10, 26.67))
                        ),
                        6,
                        "Bg001.png", 
                        2),
    "Singapore": (6000, (("Doge", 150, -1, ("start", 0), (4, 10)), 
                         ("Doge", 150, -1, ("start", 30), (6, 30)), 
                         ("Snache", 150, -1, ("start", 60), (10, 30)), 
                         ("ThoseGuys", 150, -1, ("start", 90), (10, 30)), 
                         ("ThoseGuys", 150, 20, ("hp", 60), (0.07, 0.13))
                        ),
                        10,
                        "Bg000.png", 
                        3),
    "Dubai": (10000, (("Doge", 150, -1, ("start", 0), (6.67, 13.33)),
                      ("Snache", 150, -1, ("start", 20), (6.67, 13.33)),
                      ("ThoseGuys", 150, -1, ("start", 40), (6.67, 13.33)),
                      ("ThoseGuys", 150, 6, ("hp", 90), (2, 4)),
                      ("JackiePeng", 150, 1, ("hp", 90), (0, 0)),
                      ("ThoseGuys", 150, -1, ("hp", 88), (3.33 - 13.33)), 
                      ("JackiePeng", 150, 1, ("hp", 88), (0, 0)),
                    ), 
                    12,
                    "Bg005.png", 
                    3),
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
                             "Bg002.png",
                             4),
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
                       "Bg002.png",
                       5),
    "Monaco": (30000, (("Doge", 150, -1, ("start", 0), (1, 10)),
                       ("Snache", 150, -1, ("start", 0), (1, 10)),
                       ("ThoseGuys", 150, -1, ("start", 20), (1, 2)),
                       ("Hippoe", 150, 1, ("start", 40), (0, 0)),
                       ("BaaBaa", 150, -1, ("hp", 50), (4.33, 8)),
                       ("JackiePeng", 150, -1, ("hp", 50), (4.33, 8)),
                       ),
                       5,
                       "Bg005.png",
                       6),
    "Denmark": (36000, (("Doge", 150, -1, ("start", 0), (3.33, 30)),
                        ("Snache", 150, -1, ("start", 10), (10, 20)),
                        ("ThoseGuys", 150, -1, ("start", 20), (10, 10)),
                        ("Croco", 150, -1, ("start", 40), (10, 40)),
                        ("LeBoin", 150, -2, ("hp", 90), 0),
                        ("ThoseGuys", 150, -1, ("hp", 90), (0.07, 1)),
                        ("ThoseGuys", 150, 20, ("hp", 90), (0.07, 0.07)),
                        ),
                        10,
                        "Bg000.png",
                        7),
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
                       "Bg000.png",
                       8),
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
                         "Bg000.png",
                         9),
    "Easter Island": (40000, (("ThoseGuys", 150, -1, ("start", 0), (1, 10)),
                              ("Croco", 150, -1, ("start", 20), (10, 30)),
                              ("SquireRels", 150, -1, ("start", 0), (1, 16.67)),
                              ("OneHorn", 150, 1, ("start", 0), (0, 0)),
                              ("OneHorn", 150, -2, ("hp", 80), (0, 0)),
                              ),
                              10,
                              "Bg000.png",
                              10),
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
                         "Bg000.png",
                         10),
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
                      "Bg006.png",
                      10)
}

# def playAudio(name):
attackSound = pygame.mixer.Sound('Sounds/bcAttack.ogg')
attackBaseSound = pygame.mixer.Sound('Sounds/bcAttackBase.ogg')
blockSound = pygame.mixer.Sound('Sounds/bcBlock.ogg')
bossShockwaveSound = pygame.mixer.Sound('Sounds/bcBossShockwave.ogg')
clickSound = pygame.mixer.Sound('Sounds/bcClick.ogg')
defeatSound = pygame.mixer.Sound('Sounds/bcDefeat.ogg')
deploySound = pygame.mixer.Sound('Sounds/bcDeploy.ogg')
enterBattleSound = pygame.mixer.Sound('Sounds/bcEnterBattle.ogg')
rewardSound = pygame.mixer.Sound('Sounds/bcReward.ogg')
scrollingSound = pygame.mixer.Sound('Sounds/bcScrolling.ogg')
unitDiesSound = pygame.mixer.Sound('Sounds/bcUnitDies.ogg')
unitRecharged = pygame.mixer.Sound('Sounds/bcUnitRecharge.ogg')
victory = pygame.mixer.Sound('Sounds/bcVictory.ogg')

normalBattleMusic = pygame.mixer.Sound('Music/bcBattle1.ogg')

# pygame.mixer.music.play(-1, 0.0) #-1: play forever, 0.0 = starting point
backgroundMusicPlaying = False

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
# name, cooldown timer
hotbar = [["Cat", 60], ["Tank", 60], ["Axe", 60], ["Gross", 66], ["Cow", 60], ["Bird", 60], ["Fish", 126], ["Lizard", 306], ["Titan", 546], ["Baha", 3000]]
catCooldowns = {
    "Cat": 0, 
    "Tank": 0, 
    "Axe": 0, 
    "Gross": 0, 
    "Cow": 0, 
    "Bird": 0, 
    "Fish": 0, 
    "Lizard": 0, 
    "Titan": 0, 
    "Baha": 0
}
# side = "cat" or "enemy", name = unit's name, level
def deploy(side, name, level):
    # hotbar slot time is current time - cooldown = => then can depoly
    new_unit = Unit.Unit(side, name, level)
    if side == 'cat' and len(catDict) < 50:
        if catCooldowns[name] == 0:
            catDict.update({f'{name}{catAmt+1}': new_unit})
            for i in hotbar:
                if i[0] == name:
                    catCooldowns[name] = i[1]
                    break
            deploySound.play()
            return True
        else:
            blockSound.play()
    else: 
        enemyDict.update({f'{name}{enemyAmt+1}': new_unit})
    return False
    # set hotbar list index thingy to current time

def menuNav(direction):
    # for arrows
    print(f"menuNav: {direction}")

workerCatLevel = 0
def upgradeWorkerCat():
    print("upgrade worker cat")
    
def isPressed(key):
    if key[1]:
        return True

def hpTriggerCheck(value):
    if value == "hp":
        True

currentStage = "Korea"
inStage = True
currentMoney = 0
enemies = [
    [startTime, lastTime, interval]
] # times for finding intervals
# startTime = "start", "hp", "boss"
currentOpponentBaseHp= 0
currentBaseHp = 0
<<<<<<< HEAD
# def playStage(currentStage):
#     for i in range(stages[currentStage][1].length):
#         enemies.append([])
=======
catDict = {}
enemyDict = {}
catAmt = 0
enemyAmt = 0
catPos = {}
enemyPos = {}
# def playStage(currentStage):
#     for i in range(stages[currentStage][1].length):
#         currentEnemies.append([])
>>>>>>> origin/unitClassmaking
#     currentMoney = 0
#     richCatLevel = 0
#     currentOpponentBaseHp = stages[currentStage][0]
#     stageStartTime = time.time()
#     enterBattleSound.play()
<<<<<<< HEAD

#     while inStage:
#         for i in range(enemies):
#             if int(time.time() - stageStartTime) in enemies:
#                 print()
numOfEnemies = 0
STAGESTAGE = 0
STAGESTATES = ["start"]
'''
    "start"
    "hp"
    "boss"
'''
boss = False
listOfBasehps = [[], [], []]
def basehpcheck(value):
    if value[3][0] == "hp":
        return True
def initStage(currentStage):
    for i in range(stages[currentStage][1].length):
        enemies.append([])
    currentMoney = 0
    richCatLevel = 0
    currentOpponentBaseHp = stages[currentStage][0]
    numOfEnemies = 0
    stageStartTime = time.time()
    STAGESTAGE = 0
    STAGESTATES = "STAGE"
    boss = False
    enterBattleSound.play()

    listOfBasehps = list(filter(basehpcheck, stages[currentStage][1]))[3][1] # gets 0-100 values
=======

#     while inStage:
#         for i in range(currentEnemies):
#             if int(time.time() - stageStartTime) in currentEnemies:
#                 print()
>>>>>>> origin/unitClassmaking

    return enemies


# =================================
#            MAIN LOOP
# =================================
enterBattleSound.play()
while True:
    if not backgroundMusicPlaying:
        normalBattleMusic.play(-1)
        backgroundMusicPlaying = True
    screen.fill("red")
    catPos = {}
    if len(catDict) > 0:
        print(len(catDict))
    if len(catDict) > 0:
        for i in (catDict):
            display = catDict[i].unitUpdate(enemyPos)
            catPos.update({i: display["hitbox"]})
            screen.blit(display["animation"], display["displayPos"])
            catDict[i].unitDetectionUpdate(enemyPos)
            if display["attack?"]:
                for i in display["targets"]:
                    if enemyDict[i].takeDamage(display["damage"]):
                        del enemyDict[i]
                        del enemyPos[i]
    enemyPos = {}
    if len(enemyDict) > 0:
        for i in (enemyDict):
            display = enemyDict[i].unitUpdate(catPos)
            enemyPos.update({i: display["hitbox"]})
            screen.blit(display["animation"], display["displayPos"])
            enemyDict[i].unitDetectionUpdate(catPos)
            if display["attack?"]:
                for i in display["targets"]:
                    if catDict[i].takeDamage(display["damage"]):
                        del catDict[i]
                        del catPos[i]
    if len(catDict) > 0:
        for i in (catDict):
            catDict[i].unitDetectionUpdate(enemyPos)
    if len(enemyDict) > 0:
        for i in (enemyDict):
            enemyDict[i].unitDetectionUpdate(catPos)

    for i in catCooldowns:
        if catCooldowns[i] > 0:
            catCooldowns[i] -= 1
    # key press detection
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
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # QWERT
            # ASDFG
            # general navigation w/ enter & arrow keys
            if event.key == K_q:
                keyPressedBoolean[0][1] = True
            if event.key == K_w:
                keyPressedBoolean[1][1] = True
            if event.key == K_e:
                keyPressedBoolean[2][1] = True
            if event.key == K_r:
                keyPressedBoolean[3][1] = True
            if event.key == K_t:
                keyPressedBoolean[4][1] = True
            if event.key == K_a:
                keyPressedBoolean[5][1] = True
            if event.key == K_s:
                keyPressedBoolean[6][1] = True
            if event.key == K_d:
                keyPressedBoolean[7][1] = True
            if event.key == K_f:
                keyPressedBoolean[8][1] = True
            if event.key == K_g:
                keyPressedBoolean[9][1] = True
            if event.key == K_RETURN:
                keyPressedBoolean[10][1] = True
            if event.key == K_UP:
                keyPressedBoolean[11][1] = True
            if event.key == K_DOWN:
                keyPressedBoolean[12][1] = True
            if event.key == K_LEFT:
                keyPressedBoolean[13][1] = True
            if event.key == K_RIGHT:
                keyPressedBoolean[14][1] = True
            if event.key == K_TAB:
                keyPressedBoolean[15][1] = True
                
            # for exitting program /w keyboard shortcut
            if event.key == K_ESCAPE:
                if GAMESTATE == "PAUSE":
                    GAMESTATE = "STAGE"
                else:
                    GAMESTATE = "PAUSE"
                print(GAMESTATE)
            if event.key == K_F4:
                pygame.quit()   
                sys.exit()

    currentKeyPresses = list(filter(isPressed, keyPressedBoolean))
    match GAMESTATE:
        case "STAGE":
            catLevel = stages[currentStage][4]
            for every in currentKeyPresses:
                match every[0]:
                    case "q":
                        catAmt += (1 if deploy("cat", hotbar[0][0], catLevel) else 0)
                    case "w":
                        catAmt += (1 if deploy("cat", hotbar[1][0], catLevel) else 0)
                    case "e":
                        catAmt += (1 if deploy("cat", hotbar[2][0], catLevel) else 0)
                    case "r":
                        catAmt += (1 if deploy("cat", hotbar[3][0], catLevel) else 0)
                    case "t":
                        catAmt += (1 if deploy("cat", hotbar[4][0], catLevel) else 0)
                    case "a":
                        catAmt += (1 if deploy("cat", hotbar[5][0], catLevel) else 0)
                    case "s":
                        catAmt += (1 if deploy("cat", hotbar[6][0], catLevel) else 0)
                    case "d":
                        catAmt += (1 if deploy("cat", hotbar[7][0], catLevel) else 0)
                    case "f":
                        catAmt += (1 if deploy("cat", hotbar[8][0], catLevel) else 0)
                    case "g":
                        catAmt += (1 if deploy("cat", hotbar[9][0], catLevel) else 0)
                    case "tab":
                        upgradeWorkerCat()
                    case _:
                        blockSound.play()
<<<<<<< HEAD
            if inStage:
                if STAGESTAGE == 0: #done
                    enemies = initStage()
                if listOfBasehps: #done
                    if listOfBasehps[0] > currentBaseHp/stages[currentStage][0]*100 > listOfBasehps[1]:
                        currentHpEnemies = list(filter(hpTriggerCheck, enemies))
                        for i in currentHpEnemies:
                            currentEnemies.append(i)
                        del listOfBasehps[0]
                if "boss" in STAGESTATES: #done
                    STAGESTATES = "boss"
                    lastBossTime = time.time()
                currentEnemies = list(filter(lambda enemy: enemy[2] == "start" and enemy[]-enemy[2] == time.time(), enemies))
                match STAGESTATES:
                    case "start":
                        currentEnemies = list(filter(lambda enemy: enemy[2] == "start" and enemy[]-enemy[2] == time.time(), enemies))
                    case "hp":
                        currentEnemies = list(filter(lambda enemy: enemy[2] == "hp" and enemy[]-enemy[2] == time.time(), enemies))
                    case "boss":
                        currentEnemies = list(filter(lambda enemy: enemy[2] == "boss" and enemy[]-enemy[2] == time.time(), enemies))
                if currentEnemies and numOfEnemies<=stages[2]: # checks if list is empty and is under enemy unit cap
                    for i in range(currentEnemies):
                        deploy("enemy", currentEnemies[0], currentEnemies[1])
                STAGESTAGE += 1
                    
        case _:
            for every in currentKeyPresses:
                match every[0]:
                    case "":
                        print()
=======
            if not inStage:
                print()
                
>>>>>>> origin/unitClassmaking
        
    # start screen -> go directly to cat base screen
        # only have START, UPGRADE, xp bar (top right)
    #     # If doing gacha add catfood, rare cat capcule button
    

    # Gameplay

    # end screen

    pygame.display.update()
    fpsClock.tick(fps)