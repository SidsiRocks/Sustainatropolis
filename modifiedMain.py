import pygame as pg 
from game.game import MainGameScene
from pygame.locals import *
import pygame_gui

from game.startMenuScene import StartMenuScene

def main():
    flag = FULLSCREEN | DOUBLEBUF

    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((0,0),flag,vsync=True)
    clock = pg.time.Clock()

    startScene = StartMenuScene(screen,clock)

    option = startScene.run()
    print("Option is:",option)

if __name__ == "__main__":
    main()