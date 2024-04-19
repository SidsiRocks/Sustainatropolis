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

from pygame_gui.core import ObjectID


class StartMenuScene:
    def __init__(self,screen,clock):
        self.screen = screen
        self.playing = True
        self.clock = clock
        self.width,self.height = self.screen.get_size() 
        self.manager = pygame_gui.UIManager((self.width,self.height))

        self.loadFonts()
        self.manager.get_theme().load_theme("res/json/startMenuTheme.json")

        self.buttonWidth = 250
        self.buttonHeight = 80
        self.padY = 35
        self.option = None

        self.startButton,self.newGameButton,self.HighScoreButton, self.quitButton = self.createStartUI()

        self.backGroundImage = pg.image.load("res/graphics/backgroundImage/BG1.png").convert_alpha()
        self.backGroundImage = pg.transform.scale(self.backGroundImage,(self.width,self.height))  
        #   bg_image = pg.transform.scale(bg_image,(screen_width,screen_height))
    #can remove from loadFonts from other place
    def createStartUI(self):
        noButtons = 4
        subSectionHeight = self.buttonHeight * noButtons + self.padY * (noButtons - 1)
        subSectionWidth = self.buttonWidth

        top = (self.height - subSectionHeight)/2
        left = (self.width - subSectionWidth)/2

        startRect = Rect(left,top,self.buttonWidth,self.buttonHeight)
        newGameRect = Rect(left,top+self.buttonHeight+self.padY,self.buttonWidth,self.buttonHeight)
        HighScoreGameRect = Rect(left,top+2*self.buttonHeight+2*self.padY,self.buttonWidth,self.buttonHeight)    
        quitRect = Rect(left,top+3*self.buttonHeight+3*self.padY,self.buttonWidth,self.buttonHeight)

        startButton   = UIButton(relative_rect=startRect,text="Start",manager=self.manager,object_id=ObjectID("#startButton","@startMenuButtons"))
        newGameButton = UIButton(relative_rect=newGameRect,text="New Game",manager=self.manager,object_id=ObjectID("#newGameButton","@startMenuButtons")) 
        HighScoreButton    = UIButton(relative_rect=HighScoreGameRect,text="High Score",manager=self.manager,object_id=ObjectID("#HighScoreButton","@startMenuButtons"))
        quitButton    = UIButton(relative_rect=quitRect,text="Quit",manager=self.manager,object_id=ObjectID("#quitButton","@startMenuButtons"))

        return startButton,newGameButton,HighScoreButton,quitButton
    def loadFonts(self):
        self.manager.add_font_paths("Montserrat",
                                    "./res/fonts/Montserrat-Regular.ttf",
                                    "./res/fonts/Montserrat-Bold.ttf",
                                    "./res/fonts/Montserrat-Italic.ttf",
                                    "./res/fonts/Montserrat-BoldItalic.ttf")
        self.manager.preload_fonts([
            {'name':'Montserrat','html_size':'6','style':'bold'},
            {'name':'Montserrat','html_size':'4','style':'regular'}
        ])
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
                    self.playing = False
                elif event.ui_element == self.newGameButton:
                    print("Start a new game")
                    self.option = "New game"
                    self.playing = False
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