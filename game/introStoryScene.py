import pygame as pg
from .util import ldImage
from .settings import TILE_SIZE


import sys
import pygame_gui 
from pygame import Rect
from pygame_gui.elements.ui_button import UIButton

from pygame_gui.core import ObjectID



class IntroStoryStoryScene:
    def __init__(self,screen,clock):
        self.screen = screen
        self.playing = True
        self.clock = clock 
        self.width,self.height = self.screen.get_size()

        self.manager = pygame_gui.UIManager((self.width,self.height))
        
        self.loadFonts()
        self.manager.get_theme().load_theme("res/json/startMenuTheme.json")

        self.nextPageBtnSize = (100,80)

        self.padY = 30
        self.padX = 30
        nextButtonRect = Rect(self.width-self.nextPageBtnSize[0]-self.padX,
                              self.height-self.nextPageBtnSize[1]-self.padY,
                              self.nextPageBtnSize[0],self.nextPageBtnSize[1])
        #nextButtonRect = Rect(0,0,self.nextPageBtnSize[0],self.nextPageBtnSize[1])
        self.nextButton = UIButton(relative_rect=nextButtonRect,text="Next",
                                   manager=self.manager,
                                   object_id=
                                   ObjectID("@startMenuButtons","#nextStoryButton"))

        self.storyImagePaths = ["res/graphics/Page1.png","res/graphics/Page2.png","res/graphics/Page3.png"]
        self.storyImages =  self.loadStoryImages()
        self.curStoryIndx = 0
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
    
    def loadStoryImages(self):
        result = []
        for path in self.storyImagePaths:
            curImg = ldImage(path)
            result.append(curImg)
        return result

    def run(self):
        while self.playing:
            self.clock.tick(60)
            self.draw()
            self.events()

    def events(self):
        self.timeDelta = self.clock.tick(60)/1000

        eventList = pg.event.get()
        for event in eventList:
            if event.type == pg.QUIT:
                self.quitScene()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.nextButton:
                    print("Clicked on next button")
                    self.updateNewStoryImage()
            self.manager.process_events(event)
        self.manager.update(self.timeDelta)
    def updateNewStoryImage(self):
        self.curStoryIndx += 1
        if self.curStoryIndx == len(self.storyImages):
            self.quitScene()
    def quitScene(self):
        self.playing = False    
    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.storyImages[self.curStoryIndx],(0,0))
        self.manager.draw_ui(self.screen)
        pg.display.flip()    
