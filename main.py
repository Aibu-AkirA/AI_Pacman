import sys
import pygame
from pygame.locals import *

global screen
global background
pygame.init()

screen = pygame.display.set_mode((600, 600))
background = pygame.image.load("./image/mainScreen.jpg")
pygame.display.set_caption("PAC-MAN")


def main():

    while True:
        pygame.display.update()
        screen.blit(background, (0, 0))
        for event2 in pygame.event.get():
            if event2.type == QUIT:
                pygame.quit()
                sys.exit

    pygame.quit()
    sys.exit


if __name__ == '__main__':
    main()
