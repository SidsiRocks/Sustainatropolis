import pygame 
from pygame import Rect

from pygame_gui.core import ObjectID

from .statisticsUI import StatisticsWindow
from .projectsUI import ProjectsUI
from .notificationsBoxUI import NotificationsBoxUI
from .turnBarUI import TurnBarUI
from .settingsUI import SettingsUI
from .explanationUI import ExplanationUI

def createId(txt):
    return ObjectID(class_id="@"+txt,object_id="#"+txt)


class MainGameUI:
    def __init__(self,manager,themePath,world,game):
        #have to create manager correctly
        self.manager = manager
        self.loadTheme(themePath)
        self.statsWindowWrapper = StatisticsWindow(manager)
        self.turnBar = TurnBarUI(manager,game)
        self.notificationBox = NotificationsBoxUI(manager)
        self.projectUIWrapper = ProjectsUI(manager,self.statsWindowWrapper.statsWindow,self.notificationBox)
        self.projectUIWrapper.setWorld(world)
        self.projectUIWrapper.setGame(game)

        self.settingsUI = SettingsUI(manager,game.audioManager)
        self.explainUI = ExplanationUI(manager)
    def loadTheme(self,themePath):
        self.manager.get_theme().load_theme(themePath)
    
    def update(self):
        self.settingsUI.update()

    def processEvents(self,event,audioManager):
        self.projectUIWrapper.processEvent(event)
        self.turnBar.processEvents(event,self,audioManager)
        self.settingsUI.processEvent(event)
        self.explainUI.processEvent(event)