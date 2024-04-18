import pygame as pg
from .gameWorldAlt import GameData
from .util import drawDebugText,isoCoordToRenderPos,isoRenderPosToImgRenderPos,changeOfBasis,basisVecX,basisVecY
from .settings import TILE_SIZE
from .powerManagement import PowerManagement
from .waterManagement import WaterManagement
from .camera import Camera

import sys
import pygame_gui 
from game.mainGameUI import MainGameUI
from pygame import Rect
from pygame_gui.elements.ui_button import UIButton
from .audio import AudioManager
from .groundRender import GroundRender
from .renderTreeRock import RockTreeRender


class StartMenuScene:
    def __init__(self,screen,clock):
        self.screen = screen
        self.playing = True
        self.clock = clock
        self.width,self.height = self.screen.get_size() 
        self.manager = pygame_gui.UIManager((self.width,self.height))

        self.buttonWidth = 250
        self.buttonHeight = 80
        self.padY = 50
        self.option = None

        self.startButton,self.newGameButton,self.quitButton = self.createStartUI()

        self.backGroundImage = pg.image.load("res/graphics/backgroundImage/ScreenShotSlightBlur.png").convert_alpha()

    #can remove from loadFonts from other place
    def createStartUI(self):
        noButtons = 3
        subSectionHeight = self.buttonHeight * noButtons + self.padY * (noButtons - 1)
        subSectionWidth = self.buttonWidth

        top = (self.height - subSectionHeight)/2
        left = (self.width - subSectionWidth)/2

        startRect = Rect(left,top,self.buttonWidth,self.buttonHeight)
        newGameRect = Rect(left,top+self.buttonHeight+self.padY,self.buttonWidth,self.buttonHeight)
        quitRect = Rect(left,top+2*self.buttonHeight+2*self.padY,self.buttonWidth,self.buttonHeight)

        startButton   = UIButton(relative_rect=startRect,text="Start",manager=self.manager)
        newGameButton = UIButton(relative_rect=newGameRect,text="New Game",manager=self.manager) 
        quitButton    = UIButton(relative_rect=quitRect,text="Quit",manager=self.manager)

        return startButton,newGameButton,quitButton
    def loadFonts(self):
        pass 
    def run(self):
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
        return self.option
    def events(self):
        self.timeDelta = self.clock.tick(60)/1000
        
        eventList = pg.event.get()
        for event in eventList:
            if event.type == pg.QUIT:
                self.quitScene()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quitScene()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.startButton:
                    print("Stating game now")
                    self.option = "Load game" 
                elif event.ui_element == self.newGameButton:
                    print("Start a new game")
                    self.option = "New game"
                elif event.ui_element == self.quitButton:
                    self.quitScene()
            self.manager.process_events(event)
               #handle start button new game button and quit button here
        self.manager.update(self.timeDelta)
    def update(self):
        pass
    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.backGroundImage,(0,0))
        self.manager.draw_ui(self.screen)
        pg.display.flip()
    def quitScene(self):
        pg.quit()
        sys.exit()