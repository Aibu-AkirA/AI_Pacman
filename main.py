import sys
import pygame
from pygame.locals import *
import time
import re

pygame.init()

screen = pygame.display.set_mode((600, 600))
background = pygame.image.load("./image/mainScreen.jpg")
pygame.display.set_caption("PAC-MAN")
pac_image = pygame.image.load("./image/pac_man600.png")
cookie_image = pygame.image.load("./image/cookie600.png")
cookieBig_image = pygame.image.load("./image/cookie_Big600.png")

# Start screen
startScreen = 59
startCenter = [270, 282]
gameStage = 1

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
    global startScreen
    time.sleep(sleepTime)
    startScreen -= 1
    return pygame.image.load("./image/" + cSS + size_L + num + ".png")


def playGame(pacNext_XY, pacNext_Value, size_L, getDir):
    global pac_image, imgCount, pacOld_Dir
    global cookiePosition, cookieBigPosition
    global gameStage, startScreen

    while gameStage != 6:

        if startScreen > 59:
            start_img = startImgRe(0.15, "clear", size_L[4])

        elif startScreen > 49:
            start_img = startImgRe(0.15, "stage", size_L[4],  "0")

        elif startScreen > 39:
            start_img = startImgRe(0.07, "stage", size_L[4],  str(gameStage))

        elif startScreen > 0:
            start_img = startImgRe(0.08, "start", size_L[4], str(int(startScreen / 10)))

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
            # -----------------------------cookie-------------------------------
            if str(pacNow_Pos2rP) in cookiePosition:
                cookiePosition.remove(str(pacNow_Pos2rP))

            if str(pacNow_Pos2rP) in cookieBigPosition:
                cookieBigPosition.remove(str(pacNow_Pos2rP))
                # ghost_RunTime = 150

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

        # ---- image reset ----

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
