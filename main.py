import pygame as pg 
from game.game import MainGameScene
from pygame.locals import *

def main():
#    flag = FULLSCREEN | DOUBLEBUF 
    flag = DOUBLEBUF
    running = True 

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((1200,800),flag,vsync=True)
#    screen = pg.display.set_mode((0,0),flag,vsync=True)
    clock = pg.time.Clock()

    game = MainGameScene(screen,clock)
    while running:
        game.run()

if __name__ == "__main__":
    main()