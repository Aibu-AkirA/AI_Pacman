import sys
import pygame
from pygame.locals import *
import time
import re
import random
import math

pygame.init()

screen = pygame.display.set_mode((600, 600))
background = pygame.image.load("./image/mainScreen.jpg")
pygame.display.set_caption("PAC-MAN")
pac_image = pygame.image.load("./image/pac_man600.png")
red_image = pygame.image.load("./image/Red6000ri.png")
blue_image = pygame.image.load("./image/Blue6000ri.png")
yellow_image = pygame.image.load("./image/yellow6000ri.png")
pink_image = pygame.image.load("./image/Pink6000ri.png")
cookie_image = pygame.image.load("./image/cookie600.png")
cookieBig_image = pygame.image.load("./image/cookie_Big600.png")

# Start screen
startScreen = 59
startCenter = [270, 282]
gameStage = 1
start_img = ""

# Pacman data
x, y = 261, 333
pacNow_Pos = [x, y]
pacNow_Pos2rP = [0, 0]
pacNext_Pos = [x, y]
pacNext_Pos2rP = [0, 0]  # rP is roadPosition
pacOld_Move = [0, -6]
pacOld_Pos = [x, y]
pacOld_Pos2rP = [0, 0]  # rP is roadPosition
pacOld_Dir = 'le'

imgCount = 1
imgList = ['1', '2', '3', '1', '2']
sizeList = [3, 6, 540, 594, "600"]

# Red
redNow_pos = [243, 207]
redNow_pos2rP = [40, 34]
redCheck_pos2rP = [40, 34]  # rP is roadPosition
redJudgment = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
redEat = 0

# 1 left 3
# 2 down 0
# 3 right 1
# 0 up 2
red_Dir = [0, 2]
redToPac = [0, 0, 0, 0]

# Blue
blueNow_pos = [261, 207]
blueNow_pos2rP = [43, 34]
blueCheck_pos2rP = [43, 34]  # rP is roadPosition
blueJudgment = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
blueEat = 0

blue_Dir = [1, 3]
blueToPac = [0, 0, 0, 0]

# Yellow
yellowNow_pos = [279, 207]
yellowNow_pos2rP = [46, 34]
yellowCheck_pos2rP = [46, 34]  # rP is roadPosition
yellowJudgment = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
yellowEat = 0

yellow_Dir = [3, 1]
yellowToPac = [0, 0, 0, 0]

# Pink
pinkNow_pos = [297, 207]
pinkNow_pos2rP = [49, 34]
pinkCheck_pos2rP = [49, 34]  # rP is roadPosition
pinkJudgment = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
pinkEat = 0

pink_Dir = [2, 0]
pinkToPac = [0, 0, 0, 0]
pacDirIndex = ['up', 'le', 'dw', 'ri']
pinkPakDirGet = [[0, -12], [1, -12], [0, 12], [1, 12]]

# All ghosts
ghost_DirB = [2, 3, 0, 1]
ghost_DirIndex = [[1, -1], [0, -1], [1, 1], [0, 1]]
ghost_GetDir = ['up', 'le', 'dw', 'ri']

ghost_RunTime = 0
ghost_Run = [0, 0]
ghost_EatRoadPos = [48, 40]
ghostChScTime = [[],
                 [-70, 200, -70, 200, -70, 200, -50, 9999999999999999],
                 [-65, 200, -65, 200, -65, 200, -40, 9999999999999999],
                 [-60, 250, -60, 250, -60, 250, -30, 9999999999999999],
                 [-55, 250, -55, 250, -55, 250, -20, 9999999999999999],
                 [-50, 300, -50, 300, -50, 300, -10, 9999999999999999]]
ghostChScCheck = 0
ghostChScTimeIndex = 0
ghost_imgCount = 3
judgmentPlus = [[0, 1], [0, -1], [1, 0], [-1, 0]]

# ghostRoadPos
red_disperse = [82, 1]
yellow_disperse = [7, 97]
pink_disperse = [7, 1]
blue_disperse = [82, 79]

# Data of position
with open('./data/roadPosition', 'r') as f:
    roadPosition = f.read()

with open('./data/roadPositionGhost', 'r') as f:
    ghostRoadPos = f.read()

with open('./data/cookiePosition', 'r') as f:
    data = f.read()

cookiePosition = data.splitlines()
cookieBigPosition = ['[7, 22]', '[82, 22]', '[7, 91]', '[82, 91]']


def startImgRe(sleepTime, cSS, size_L, num=""):
    global startScreen, start_img
    time.sleep(sleepTime)
    startScreen -= 1
    start_img = pygame.image.load("./image/" + cSS + size_L + num + ".png")


def playGame(pacNext_XY, pacNext_Value, size_L, getDir):
    global pac_image, imgCount, pacOld_Dir
    global cookiePosition, cookieBigPosition
    global gameStage, startScreen, start_img
    global red_image, red_Dir, redEat, redNow_pos2rP
    global blue_image, blue_Dir, blueEat, blueNow_pos2rP
    global yellow_image, yellow_Dir, yellowEat, yellowNow_pos2rP
    global pink_image, pink_Dir, pinkEat, pinkNow_pos2rP
    global ghost_imgCount, ghost_RunTime, ghostChScCheck, ghostChScTimeIndex

    while gameStage != 6:

        if startScreen > 59:
            startImgRe(0.15, "clear", size_L[4])

        elif startScreen > 49:
            startImgRe(0.15, "stage", size_L[4], "0")

        elif startScreen > 39:
            startImgRe(0.07, "stage", size_L[4], str(gameStage))

        elif startScreen > 0:
            startImgRe(0.08, "start", size_L[4], str(int(startScreen / 10)))

        else:

            # -----------------------------pacman-----------------------------
            pacNext_Pos[pacNext_XY] = pacNow_Pos[pacNext_XY] + pacNext_Value
            pacNext_Pos[0] = pacNext_Pos[0] % size_L[2]
            pacNext_Pos[1] = pacNext_Pos[1] % size_L[3]

            pacNext_Pos2rP[0] = int((pacNext_Pos[0] - size_L[0]) / size_L[1])
            pacNext_Pos2rP[1] = int((pacNext_Pos[1] - size_L[0]) / size_L[1])

            pacOld_Pos[pacOld_Move[0]] = pacNow_Pos[pacOld_Move[0]] + pacOld_Move[1]
            pacOld_Pos[0] = pacOld_Pos[0] % size_L[2]
            pacOld_Pos[1] = pacOld_Pos[1] % size_L[3]
            pacOld_Pos2rP[0] = int((pacOld_Pos[0] - size_L[0]) / size_L[1])
            pacOld_Pos2rP[1] = int((pacOld_Pos[1] - size_L[0]) / size_L[1])

            time.sleep(0.06)

            if str(pacOld_Pos2rP) in roadPosition and str(pacNext_Pos2rP) not in roadPosition:

                pacNow_Pos[pacOld_Move[0]] = pacNow_Pos[pacOld_Move[0]] + pacOld_Move[1]

                pac_image = pygame.image.load("./image/pac_man" + size_L[4] + imgList[imgCount] + pacOld_Dir + ".png")
                if imgCount == 4:
                    imgCount = 0
                else:
                    imgCount += 1

                pacNext_Pos[0] = pacNow_Pos[0]
                pacNext_Pos[1] = pacNow_Pos[1]

            elif str(pacNext_Pos2rP) in roadPosition:

                pacNow_Pos[pacNext_XY] = pacNow_Pos[pacNext_XY] + pacNext_Value

                pacNow_Pos[0] = pacNow_Pos[0] % size_L[2]
                pacNow_Pos[1] = pacNow_Pos[1] % size_L[3]

                pac_image = pygame.image.load("./image/pac_man" + size_L[4] + imgList[imgCount] + getDir + ".png")
                pacOld_Dir = getDir
                if imgCount == 4:
                    imgCount = 0
                else:
                    imgCount += 1

                pacOld_Move[0] = pacNext_XY
                pacOld_Move[1] = pacNext_Value

                pacOld_Pos[0] = pacNow_Pos[0]
                pacOld_Pos[1] = pacNow_Pos[1]

            else:
                pacNext_Pos[0] = pacNow_Pos[0]
                pacNext_Pos[1] = pacNow_Pos[1]

                pacOld_Pos[0] = pacNow_Pos[0]
                pacOld_Pos[1] = pacNow_Pos[1]

            pacNow_Pos2rP[0] = int((pacNow_Pos[0] - size_L[0]) / size_L[1])
            pacNow_Pos2rP[1] = int((pacNow_Pos[1] - size_L[0]) / size_L[1])

            # -----------------------------pacman-----------------------------

            # -----------------------------red--------------------------------
            redCheck_pos2rP[0] = int((redNow_pos[0] - size_L[0]) / size_L[1])
            redCheck_pos2rP[1] = int((redNow_pos[1] - size_L[0]) / size_L[1])

            if ghostChScCheck == 0 and ghostChScTimeIndex < 8:
                ghostChScCheck = ghostChScTime[gameStage][ghostChScTimeIndex]
                ghostChScTimeIndex += 1

            if redEat == 0:
                if ghost_RunTime == 0:
                    if ghostChScCheck > 0:
                        redToPac[0] = ((pacNow_Pos2rP[0] - redCheck_pos2rP[0]) ** 2 + (
                                pacNow_Pos2rP[1] - (redCheck_pos2rP[1] - 1)) ** 2)
                        redToPac[1] = ((pacNow_Pos2rP[0] - (redCheck_pos2rP[0] - 1)) ** 2 + (
                                pacNow_Pos2rP[1] - redCheck_pos2rP[1]) ** 2)
                        redToPac[2] = ((pacNow_Pos2rP[0] - redCheck_pos2rP[0]) ** 2 + (
                                pacNow_Pos2rP[1] - (redCheck_pos2rP[1] + 1)) ** 2)
                        redToPac[3] = ((pacNow_Pos2rP[0] - (redCheck_pos2rP[0] + 1)) ** 2 + (
                                pacNow_Pos2rP[1] - redCheck_pos2rP[1]) ** 2)
                        redToPac[red_Dir[1]] = 1000000

                    else:
                        redToPac[0] = ((red_disperse[0] - redCheck_pos2rP[0]) ** 2 + (
                                red_disperse[1] - (redCheck_pos2rP[1] - 1)) ** 2)
                        redToPac[1] = ((red_disperse[0] - (redCheck_pos2rP[0] - 1)) ** 2 + (
                                red_disperse[1] - redCheck_pos2rP[1]) ** 2)
                        redToPac[2] = ((red_disperse[0] - redCheck_pos2rP[0]) ** 2 + (
                                red_disperse[1] - (redCheck_pos2rP[1] + 1)) ** 2)
                        redToPac[3] = ((red_disperse[0] - (redCheck_pos2rP[0] + 1)) ** 2 + (
                                red_disperse[1] - redCheck_pos2rP[1]) ** 2)
                        redToPac[red_Dir[1]] = 1000000

                else:
                    ghost_Run[0] = random.randrange(7, 83)
                    ghost_Run[1] = random.randrange(7, 92)
                    redToPac[0] = ((ghost_Run[0] - redCheck_pos2rP[0]) ** 2 + (
                            ghost_Run[1] - (redCheck_pos2rP[1] - 1)) ** 2)
                    redToPac[1] = ((ghost_Run[0] - (redCheck_pos2rP[0] - 1)) ** 2 + (
                            ghost_Run[1] - redCheck_pos2rP[1]) ** 2)
                    redToPac[2] = ((ghost_Run[0] - redCheck_pos2rP[0]) ** 2 + (
                            ghost_Run[1] - (redCheck_pos2rP[1] + 1)) ** 2)
                    redToPac[3] = ((ghost_Run[0] - (redCheck_pos2rP[0] + 1)) ** 2 + (
                            ghost_Run[1] - redCheck_pos2rP[1]) ** 2)
                    redToPac[red_Dir[1]] = 1000000

                for i in range(4):
                    redCheck_pos2rP[0] = redNow_pos2rP[0]
                    redCheck_pos2rP[1] = redNow_pos2rP[1]
                    redCheck_pos2rP[ghost_DirIndex[i][0]] = redNow_pos2rP[ghost_DirIndex[i][0]] + ghost_DirIndex[i][1]

                    if str(redCheck_pos2rP) not in ghostRoadPos:
                        redToPac[i] = 1000000

                if redToPac.count(1000000) == 4:
                    red_Dir[0], red_Dir[1] = red_Dir[1], red_Dir[0]
                else:
                    red_Dir[0] = redToPac.index(min(redToPac))
                    red_Dir[1] = ghost_DirB[redToPac.index(min(redToPac))]

                redNow_pos2rP[ghost_DirIndex[red_Dir[0]][0]] = redNow_pos2rP[ghost_DirIndex[red_Dir[0]][0]] + ghost_DirIndex[red_Dir[0]][1]

            else:
                redEat -= 1
                if redEat == 1 or redEat == 0:
                    redNow_pos2rP = [40, 34]
                    red_Dir[0] = 3
                    red_Dir[1] = 1
                else:
                    redNow_pos2rP = [38, 40]

            if ghost_RunTime == 0:
                red_image = pygame.image.load(
                    "./image/Red" + size_L[4] + str(ghost_imgCount % 2) + ghost_GetDir[red_Dir[0]] + ".png")
            else:
                red_image = pygame.image.load("./image/ghost" + size_L[4] + str(ghost_imgCount % 2) + ".png")

            redNow_pos[0] = redNow_pos2rP[0] * size_L[1] + size_L[0]
            redNow_pos[1] = redNow_pos2rP[1] * size_L[1] + size_L[0]
            # -----------------------------red--------------------------------
            # -----------------------------blue-------------------------------
            blueCheck_pos2rP[0] = int((blueNow_pos[0] - size_L[0]) / size_L[1])
            blueCheck_pos2rP[1] = int((blueNow_pos[1] - size_L[0]) / size_L[1])

            blue_target = [0, 0]
            blue_target[0] = abs(pacNow_Pos2rP[0]) - abs(redCheck_pos2rP[0])
            blue_target[1] = abs(pacNow_Pos2rP[1]) - abs(redCheck_pos2rP[1])

            blue_target[0] = abs(pacNow_Pos2rP[0]) - abs(blue_target[0])
            blue_target[1] = abs(pacNow_Pos2rP[1]) - abs(blue_target[1])

            if blueEat == 0:
                if ghost_RunTime == 0:
                    if ghostChScCheck > 0:
                        blueToPac[0] = ((blue_target[0] - blueCheck_pos2rP[0]) ** 2 + (
                                    blue_target[1] - (blueCheck_pos2rP[1] - 1)) ** 2)
                        blueToPac[1] = ((blue_target[0] - (blueCheck_pos2rP[0] - 1)) ** 2 + (
                                    blue_target[1] - blueCheck_pos2rP[1]) ** 2)
                        blueToPac[2] = ((blue_target[0] - blueCheck_pos2rP[0]) ** 2 + (
                                    blue_target[1] - (blueCheck_pos2rP[1] + 1)) ** 2)
                        blueToPac[3] = ((blue_target[0] - (blueCheck_pos2rP[0] + 1)) ** 2 + (
                                    blue_target[1] - blueCheck_pos2rP[1]) ** 2)
                        blueToPac[blue_Dir[1]] = 1000000

                    else:
                        blueToPac[0] = ((blue_disperse[0] - blueCheck_pos2rP[0]) ** 2 + (
                                    blue_disperse[1] - (blueCheck_pos2rP[1] - 1)) ** 2)
                        blueToPac[1] = ((blue_disperse[0] - (blueCheck_pos2rP[0] - 1)) ** 2 + (
                                    blue_disperse[1] - blueCheck_pos2rP[1]) ** 2)
                        blueToPac[2] = ((blue_disperse[0] - blueCheck_pos2rP[0]) ** 2 + (
                                    blue_disperse[1] - (blueCheck_pos2rP[1] + 1)) ** 2)
                        blueToPac[3] = ((blue_disperse[0] - (blueCheck_pos2rP[0] + 1)) ** 2 + (
                                    blue_disperse[1] - blueCheck_pos2rP[1]) ** 2)
                        blueToPac[blue_Dir[1]] = 1000000

                else:
                    ghost_Run[0] = random.randrange(7, 83)
                    ghost_Run[1] = random.randrange(7, 92)
                    blueToPac[0] = ((ghost_Run[0] - blueCheck_pos2rP[0]) ** 2 + (
                                ghost_Run[1] - (blueCheck_pos2rP[1] - 1)) ** 2)
                    blueToPac[1] = ((ghost_Run[0] - (blueCheck_pos2rP[0] - 1)) ** 2 + (
                                ghost_Run[1] - blueCheck_pos2rP[1]) ** 2)
                    blueToPac[2] = ((ghost_Run[0] - blueCheck_pos2rP[0]) ** 2 + (
                                ghost_Run[1] - (blueCheck_pos2rP[1] + 1)) ** 2)
                    blueToPac[3] = ((ghost_Run[0] - (blueCheck_pos2rP[0] + 1)) ** 2 + (
                                ghost_Run[1] - blueCheck_pos2rP[1]) ** 2)
                    blueToPac[blue_Dir[1]] = 1000000

                for i in range(4):
                    blueCheck_pos2rP[0] = blueNow_pos2rP[0]
                    blueCheck_pos2rP[1] = blueNow_pos2rP[1]
                    blueCheck_pos2rP[ghost_DirIndex[i][0]] = blueNow_pos2rP[ghost_DirIndex[i][0]] + ghost_DirIndex[i][1]

                    if str(blueCheck_pos2rP) not in ghostRoadPos:
                        blueToPac[i] = 1000000

                if blueToPac.count(1000000) == 4:
                    blue_Dir[0], blue_Dir[1] = blue_Dir[1], blue_Dir[0]

                else:
                    blue_Dir[0] = blueToPac.index(min(blueToPac))
                    blue_Dir[1] = ghost_DirB[blueToPac.index(min(blueToPac))]

                blueNow_pos2rP[ghost_DirIndex[blue_Dir[0]][0]] = blueNow_pos2rP[ghost_DirIndex[blue_Dir[0]][0]] + \
                                                                 ghost_DirIndex[blue_Dir[0]][1]

            else:
                blueEat -= 1
                if blueEat == 1 or blueEat == 0:
                    blueNow_pos2rP = [43, 34]
                    blue_Dir[0] = 3
                    blue_Dir[1] = 1
                else:
                    blueNow_pos2rP = [42, 40]

            if ghost_RunTime == 0:
                blue_image = pygame.image.load(
                    "./image/Blue" + size_L[4] + str(ghost_imgCount % 2) + ghost_GetDir[blue_Dir[0]] + ".png")

            else:
                blue_image = pygame.image.load("./image/ghost" + size_L[4] + str(ghost_imgCount % 2) + ".png")

            blueNow_pos[0] = blueNow_pos2rP[0] * size_L[1] + size_L[0]
            blueNow_pos[1] = blueNow_pos2rP[1] * size_L[1] + size_L[0]

            # -----------------------------blue-------------------------------

            # -----------------------------yellow-----------------------------
            yellowCheck_pos2rP[0] = int((yellowNow_pos[0] - size_L[0]) / size_L[1])
            yellowCheck_pos2rP[1] = int((yellowNow_pos[1] - size_L[0]) / size_L[1])

            if yellowEat == 0:
                if ghost_RunTime == 0:
                    if ghostChScCheck < 0 or int(math.sqrt((pacNow_Pos2rP[0] - yellowNow_pos2rP[0]) ** 2 + (
                            pacNow_Pos2rP[1] - (yellowNow_pos2rP[1])) ** 2)) < 24:
                        yellowToPac[0] = ((yellow_disperse[0] - yellowCheck_pos2rP[0]) ** 2 + (
                                    yellow_disperse[1] - (yellowCheck_pos2rP[1] - 1)) ** 2)
                        yellowToPac[1] = ((yellow_disperse[0] - (yellowCheck_pos2rP[0] - 1)) ** 2 + (
                                    yellow_disperse[1] - yellowCheck_pos2rP[1]) ** 2)
                        yellowToPac[2] = ((yellow_disperse[0] - yellowCheck_pos2rP[0]) ** 2 + (
                                    yellow_disperse[1] - (yellowCheck_pos2rP[1] + 1)) ** 2)
                        yellowToPac[3] = ((yellow_disperse[0] - (yellowCheck_pos2rP[0] + 1)) ** 2 + (
                                    yellow_disperse[1] - yellowCheck_pos2rP[1]) ** 2)
                        yellowToPac[yellow_Dir[1]] = 1000000

                    else:
                        yellowToPac[0] = ((pacNow_Pos2rP[0] - yellowCheck_pos2rP[0]) ** 2 + (
                                    pacNow_Pos2rP[1] - (yellowCheck_pos2rP[1] - 1)) ** 2)
                        yellowToPac[1] = ((pacNow_Pos2rP[0] - (yellowCheck_pos2rP[0] - 1)) ** 2 + (
                                    pacNow_Pos2rP[1] - yellowCheck_pos2rP[1]) ** 2)
                        yellowToPac[2] = ((pacNow_Pos2rP[0] - yellowCheck_pos2rP[0]) ** 2 + (
                                    pacNow_Pos2rP[1] - (yellowCheck_pos2rP[1] + 1)) ** 2)
                        yellowToPac[3] = ((pacNow_Pos2rP[0] - (yellowCheck_pos2rP[0] + 1)) ** 2 + (
                                    pacNow_Pos2rP[1] - yellowCheck_pos2rP[1]) ** 2)
                        yellowToPac[yellow_Dir[1]] = 1000000

                else:
                    ghost_Run[0] = random.randrange(7, 83)
                    ghost_Run[1] = random.randrange(7, 92)
                    yellowToPac[0] = ((ghost_Run[0] - yellowCheck_pos2rP[0]) ** 2 + (
                                ghost_Run[1] - (yellowCheck_pos2rP[1] - 1)) ** 2)
                    yellowToPac[1] = ((ghost_Run[0] - (yellowCheck_pos2rP[0] - 1)) ** 2 + (
                                ghost_Run[1] - yellowCheck_pos2rP[1]) ** 2)
                    yellowToPac[2] = ((ghost_Run[0] - yellowCheck_pos2rP[0]) ** 2 + (
                                ghost_Run[1] - (yellowCheck_pos2rP[1] + 1)) ** 2)
                    yellowToPac[3] = ((ghost_Run[0] - (yellowCheck_pos2rP[0] + 1)) ** 2 + (
                                ghost_Run[1] - yellowCheck_pos2rP[1]) ** 2)

                    yellowToPac[yellow_Dir[1]] = 1000000

                for i in range(4):
                    yellowCheck_pos2rP[0] = yellowNow_pos2rP[0]
                    yellowCheck_pos2rP[1] = yellowNow_pos2rP[1]
                    yellowCheck_pos2rP[ghost_DirIndex[i][0]] = yellowNow_pos2rP[ghost_DirIndex[i][0]] + \
                                                               ghost_DirIndex[i][1]

                    if str(yellowCheck_pos2rP) not in ghostRoadPos:
                        yellowToPac[i] = 1000000

                if yellowToPac.count(1000000) == 4:
                    yellow_Dir[0], yellow_Dir[1] = yellow_Dir[1], yellow_Dir[0]

                else:
                    yellow_Dir[0] = yellowToPac.index(min(yellowToPac))
                    yellow_Dir[1] = ghost_DirB[yellowToPac.index(min(yellowToPac))]

                yellowNow_pos2rP[ghost_DirIndex[yellow_Dir[0]][0]] = yellowNow_pos2rP[
                                                                         ghost_DirIndex[yellow_Dir[0]][0]] + \
                                                                     ghost_DirIndex[yellow_Dir[0]][1]
            else:
                yellowEat -= 1
                if yellowEat == 1 or yellowEat == 0:
                    yellowNow_pos2rP = [46, 34]
                    yellow_Dir[0] = 1
                    yellow_Dir[1] = 3
                else:
                    yellowNow_pos2rP = [47, 40]

            if ghost_RunTime == 0:
                yellow_image = pygame.image.load(
                    "./image/Yellow" + size_L[4] + str(ghost_imgCount % 2) + ghost_GetDir[yellow_Dir[0]] + ".png")
            else:
                yellow_image = pygame.image.load("./image/ghost" + size_L[4] + str(ghost_imgCount % 2) + ".png")

            yellowNow_pos[0] = yellowNow_pos2rP[0] * size_L[1] + size_L[0]
            yellowNow_pos[1] = yellowNow_pos2rP[1] * size_L[1] + size_L[0]
            # -----------------------------yellow-----------------------------
            # -----------------------------pink-------------------------------

            pinkCheck_pos2rP[0] = int((pinkNow_pos[0] - size_L[0]) / size_L[1])
            pinkCheck_pos2rP[1] = int((pinkNow_pos[1] - size_L[0]) / size_L[1])

            # pink_target = pacNow_Pos2rP
            # print(pink_target, pacNow_Pos2rP)

            pink_target = [0, 0]
            pink_target[0] = pacNow_Pos2rP[0]
            pink_target[1] = pacNow_Pos2rP[1]

            pink_target[pinkPakDirGet[pacDirIndex.index(getDir)][0]] = pink_target[
                                                                           pinkPakDirGet[pacDirIndex.index(getDir)][
                                                                               0]] + \
                                                                       pinkPakDirGet[pacDirIndex.index(getDir)][1]

            # print(pink_target, pacNow_Pos2rP)
            if pinkEat == 0:
                if ghost_RunTime == 0:
                    if ghostChScCheck > 0:

                        pinkToPac[0] = ((pink_target[0] - pinkCheck_pos2rP[0]) ** 2 + (
                                    pink_target[1] - (pinkCheck_pos2rP[1] - 1)) ** 2)
                        pinkToPac[1] = ((pink_target[0] - (pinkCheck_pos2rP[0] - 1)) ** 2 + (
                                    pink_target[1] - pinkCheck_pos2rP[1]) ** 2)
                        pinkToPac[2] = ((pink_target[0] - pinkCheck_pos2rP[0]) ** 2 + (
                                    pink_target[1] - (pinkCheck_pos2rP[1] + 1)) ** 2)
                        pinkToPac[3] = ((pink_target[0] - (pinkCheck_pos2rP[0] + 1)) ** 2 + (
                                    pink_target[1] - pinkCheck_pos2rP[1]) ** 2)
                        pinkToPac[pink_Dir[1]] = 1000000

                        ghostChScCheck -= 1

                    else:
                        pinkToPac[0] = ((pink_disperse[0] - pinkCheck_pos2rP[0]) ** 2 + (
                                    pink_disperse[1] - (pinkCheck_pos2rP[1] - 1)) ** 2)
                        pinkToPac[1] = ((pink_disperse[0] - (pinkCheck_pos2rP[0] - 1)) ** 2 + (
                                    pink_disperse[1] - pinkCheck_pos2rP[1]) ** 2)
                        pinkToPac[2] = ((pink_disperse[0] - pinkCheck_pos2rP[0]) ** 2 + (
                                    pink_disperse[1] - (pinkCheck_pos2rP[1] + 1)) ** 2)
                        pinkToPac[3] = ((pink_disperse[0] - (pinkCheck_pos2rP[0] + 1)) ** 2 + (
                                    pink_disperse[1] - pinkCheck_pos2rP[1]) ** 2)
                        pinkToPac[pink_Dir[1]] = 1000000

                        ghostChScCheck += 1

                else:
                    ghost_Run[0] = random.randrange(7, 83)
                    ghost_Run[1] = random.randrange(7, 92)
                    pinkToPac[0] = ((ghost_Run[0] - pinkCheck_pos2rP[0]) ** 2 + (
                                ghost_Run[1] - (pinkCheck_pos2rP[1] - 1)) ** 2)
                    pinkToPac[1] = ((ghost_Run[0] - (pinkCheck_pos2rP[0] - 1)) ** 2 + (
                                ghost_Run[1] - pinkCheck_pos2rP[1]) ** 2)
                    pinkToPac[2] = ((ghost_Run[0] - pinkCheck_pos2rP[0]) ** 2 + (
                                ghost_Run[1] - (pinkCheck_pos2rP[1] + 1)) ** 2)
                    pinkToPac[3] = ((ghost_Run[0] - (pinkCheck_pos2rP[0] + 1)) ** 2 + (
                                ghost_Run[1] - pinkCheck_pos2rP[1]) ** 2)
                    pinkToPac[pink_Dir[1]] = 1000000

                for i in range(4):
                    pinkCheck_pos2rP[0] = pinkNow_pos2rP[0]
                    pinkCheck_pos2rP[1] = pinkNow_pos2rP[1]
                    pinkCheck_pos2rP[ghost_DirIndex[i][0]] = pinkNow_pos2rP[ghost_DirIndex[i][0]] + ghost_DirIndex[i][1]

                    if str(pinkCheck_pos2rP) not in ghostRoadPos:
                        pinkToPac[i] = 1000000

                if pinkToPac.count(1000000) == 4:
                    pink_Dir[0], pink_Dir[1] = pink_Dir[1], pink_Dir[0]
                else:
                    pink_Dir[0] = pinkToPac.index(min(pinkToPac))
                    pink_Dir[1] = ghost_DirB[pinkToPac.index(min(pinkToPac))]

                pinkNow_pos2rP[ghost_DirIndex[pink_Dir[0]][0]] = pinkNow_pos2rP[ghost_DirIndex[pink_Dir[0]][0]] + \
                                                                 ghost_DirIndex[pink_Dir[0]][1]

            else:
                pinkEat -= 1
                if pinkEat == 1 or pinkEat == 0:
                    pinkNow_pos2rP = [49, 34]
                    pink_Dir[0] = 3
                    pink_Dir[1] = 1
                else:
                    pinkNow_pos2rP = [51, 40]

            if ghost_RunTime == 0:
                pink_image = pygame.image.load(
                    "./image/Pink" + size_L[4] + str(ghost_imgCount % 2) + ghost_GetDir[pink_Dir[0]] + ".png")
            else:
                pink_image = pygame.image.load("./image/ghost" + size_L[4] + str(ghost_imgCount % 2) + ".png")
                ghost_RunTime -= 1

            ghost_imgCount += 1

            pinkNow_pos[0] = pinkNow_pos2rP[0] * size_L[1] + size_L[0]
            pinkNow_pos[1] = pinkNow_pos2rP[1] * size_L[1] + size_L[0]

            # -----------------------------pink-------------------------------
            # -----------------------------cookie-------------------------------
            if str(pacNow_Pos2rP) in cookiePosition:
                cookiePosition.remove(str(pacNow_Pos2rP))

            if str(pacNow_Pos2rP) in cookieBigPosition:
                cookieBigPosition.remove(str(pacNow_Pos2rP))
                ghost_RunTime = 150

            # -----------------------------cookie-------------------------------
            if len(cookiePosition) == 0 and len(cookieBigPosition) == 0:
                pacNow_Pos[0] = (44 * size_L[1]) + size_L[0]
                pacNow_Pos[1] = (55 * size_L[1]) + size_L[0]
                pacNext_Pos[0] = pacNow_Pos[0]
                pacOld_Pos[1] = pacNow_Pos[1]
                pacOld_Pos[0] = pacNow_Pos[0]
                pacOld_Pos[1] = pacNow_Pos[1]

                startScreen = 69
                gameStage += 1

                cookiePosition = data.splitlines()

        # -----------------------------clear-------------------------------
        if len(cookiePosition) == 0 and len(cookieBigPosition) == 0:
            pacNow_Pos[0] = (44 * size_L[1]) + size_L[0]
            pacNow_Pos[1] = (55 * size_L[1]) + size_L[0]
            pacNext_Pos[0] = pacNow_Pos[0]
            pacOld_Pos[1] = pacNow_Pos[1]
            pacOld_Pos[0] = pacNow_Pos[0]
            pacOld_Pos[1] = pacNow_Pos[1]

            redNow_pos[0] = (40 * size_L[1]) + size_L[0]
            redNow_pos[1] = (34 * size_L[1]) + size_L[0]
            redNow_pos2rP[0] = 40
            redNow_pos2rP[1] = 34
            red_Dir = [0, 2]
            redEat = 0

            blueNow_pos[0] = (43 * size_L[1]) + size_L[0]
            blueNow_pos[1] = (34 * size_L[1]) + size_L[0]
            blueNow_pos2rP[0] = 43
            blueNow_pos2rP[1] = 34
            blue_Dir = [1, 3]
            blueEat = 0

            yellowNow_pos[0] = (46 * size_L[1]) + size_L[0]
            yellowNow_pos[1] = (34 * size_L[1]) + size_L[0]
            yellowNow_pos2rP[0] = 46
            yellowNow_pos2rP[1] = 34
            yellow_Dir = [3, 1]
            yellowEat = 0

            pinkNow_pos[0] = (49 * size_L[1]) + size_L[0]
            pinkNow_pos[1] = (34 * size_L[1]) + size_L[0]
            pinkNow_pos2rP[0] = 49
            pinkNow_pos2rP[1] = 34
            pink_Dir = [2, 0]
            pinkEat = 0

            ghostChScCheck = 0
            ghostChScTimeIndex = 0
            ghost_RunTime = 0
            ghost_imgCount = 3

            startScreen = 69
            gameStage += 1

            cookiePosition = data.splitlines()

            cookieBigPosition = ['[7, 22]', '[82, 22]', '[7, 91]', '[82, 91]']

            start_img = pygame.image.load("./image/clear" + size_L[4] + ".png")

        # ---- image reset ----

        pac_rect = pac_image.get_rect()
        pac_rect.center = pacNow_Pos

        red_rect = red_image.get_rect()
        red_rect.center = redNow_pos

        blue_rect = blue_image.get_rect()
        blue_rect.center = blueNow_pos

        yellow_rect = yellow_image.get_rect()
        yellow_rect.center = yellowNow_pos

        pink_rect = pink_image.get_rect()
        pink_rect.center = pinkNow_pos

        cookie_rect = cookie_image.get_rect()
        cookieBig_rect = cookieBig_image.get_rect()

        screen.blit(background, (0, 0))

        for i in cookiePosition:
            i = re.sub(r"[^ 0-9]", "", i)
            i = i.split()
            i = list(map(int, i))
            i[0] = i[0] * 6 + 3
            i[1] = i[1] * 6 + 3

            cookie_rect.center = i

            screen.blit(cookie_image, cookie_rect)

        for i in cookieBigPosition:
            i = re.sub(r"[^ 0-9]", "", i)
            i = i.split()
            i = list(map(int, i))
            i[0] = i[0] * 6 + 3
            i[1] = i[1] * 6 + 3

            cookieBig_rect.center = i

            screen.blit(cookieBig_image, cookieBig_rect)

        screen.blit(red_image, red_rect)
        screen.blit(blue_image, blue_rect)
        screen.blit(yellow_image, yellow_rect)
        screen.blit(pink_image, pink_rect)
        screen.blit(pac_image, pac_rect)
        screen.blit(pac_image, pac_rect)

        if startScreen != 0:
            start_rect = start_img.get_rect()
            start_rect.center = startCenter

            screen.blit(start_img, start_rect)

        pygame.display.update()
        # ---- image reset ----
        for event2 in pygame.event.get():
            if event2.type == QUIT:
                pygame.quit()
                sys.exit()
            if event2.type == KEYDOWN:
                if event2.key == K_LEFT:
                    playGame(0, -size_L[1], size_L, 'le')
                elif event2.key == K_RIGHT:
                    playGame(0, size_L[1], size_L, 'ri')
                elif event2.key == K_UP:
                    playGame(1, -size_L[1], size_L, 'up')
                elif event2.key == K_DOWN:
                    playGame(1, size_L[1], size_L, 'dw')


def main():
    global screen
    global background

    while True:
        pygame.display.update()
        screen.blit(background, (0, 0))
        for event2 in pygame.event.get():
            if event2.type == QUIT:
                pygame.quit()
                sys.exit()
            if event2.type == KEYUP:
                if event2.key == ord('a'):
                    screen = pygame.display.set_mode((540, 594))
                    background = pygame.image.load("./image/playScreen600.jpg")

                    pac_rect = pac_image.get_rect()
                    pac_rect.center = pacNow_Pos

                    cookie_rect = cookie_image.get_rect()
                    cookieBig_rect = cookieBig_image.get_rect()

                    screen.blit(background, (0, 0))

                    for i in cookiePosition:
                        i = re.sub(r"[^ 0-9]", "", i)
                        i = i.split()
                        i = list(map(int, i))
                        i[0] = i[0] * 6 + 3
                        i[1] = i[1] * 6 + 3

                        cookie_rect.center = i

                        screen.blit(cookie_image, cookie_rect)

                    for i in cookieBigPosition:
                        i = re.sub(r"[^ 0-9]", "", i)
                        i = i.split()
                        i = list(map(int, i))
                        i[0] = i[0] * 6 + 3
                        i[1] = i[1] * 6 + 3

                        cookieBig_rect.center = i

                        screen.blit(cookieBig_image, cookieBig_rect)
                        screen.blit(pac_image, pac_rect)

                    pygame.display.update()
                    playGame(pacOld_Move[0], pacOld_Move[1], sizeList, pacOld_Dir)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
