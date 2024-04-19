import pygame as pg 
from game.game import MainGameScene
from pygame.locals import *
import pygame_gui

from game.startMenuScene import StartMenuScene
from game.introStoryScene import IntroStoryStoryScene

def main():
    flag = FULLSCREEN | DOUBLEBUF

    pg.init()
    pg.mixer.init()

    screen = pg.display.set_mode((0,0),flag,vsync=True)
    clock = pg.time.Clock()

    startScene = StartMenuScene(screen,clock)

    while True:
        startScene.playing = True
        option = startScene.run()
        print("Option is:",option)

        turnBarFilePath = None 
        moneyFilePath = None 
        writeMaintFilePath = None 
        mapDataFilePath = None
        if option == "Load game":
            turnBarFilePath = "game/currentStartGame/turnBarYear.txt"
            moneyFilePath = "game/currentStartGame/money.txt"
            writeMaintFilePath = "game/currentStartGame/writeMaint.txt"
            mapDataFilePath = "game/currentStartGame/mapData.json"
        elif option == "New game":
            turnBarFilePath = "game/defaultStartGameData/turnBarYear.txt"
            moneyFilePath = "game/defaultStartGameData/money.txt"
            writeMaintFilePath = "game/defaultStartGameData/writeMaint.txt"
            mapDataFilePath = "game/defaultStartGameData/mapData.json"

            introScene = IntroStoryStoryScene(screen,clock)
            introScene.run()
        mainScene = MainGameScene(screen,clock,turnBarFilePath,moneyFilePath,writeMaintFilePath,mapDataFilePath)
        mainScene.run()

if __name__ == "__main__":
    main()