import pygame 
from pygame import Rect

from pygame_gui.core import ObjectID

from .statisticsUI import StatisticsWindow
from .projectsUI import ProjectsUI
from .notificationsBoxUI import NotificationsBoxUI
from .turnBarUI import TurnBarUI
from .settingsUI import SettingsUI
from .explanationUI import ExplanationUI
from .maintManager import MaintManager

def createId(txt):
    return ObjectID(class_id="@"+txt,object_id="#"+txt)


class MainGameUI:
    def __init__(self,manager,themePath,game,turnBarFilePath,writeMaintFilePath):
        #have to create manager correctly
        self.manager = manager
        self.loadTheme(themePath)
        self.statsWindowWrapper = StatisticsWindow(manager)
        self.turnBar = TurnBarUI(manager,game,turnBarFilePath)
        # self.turnBar.processEvents( None, self , game.audioManager)
        self.notificationBox = NotificationsBoxUI(manager,writeMaintFilePath)
        self.projectUIWrapper = ProjectsUI(manager,self.statsWindowWrapper.statsWindow,game,self.notificationBox,game.waterManagement)
        self.waterManager = game.waterManagement
        self.explainUI = ExplanationUI(manager)
        self.settingsUI = SettingsUI(manager,game.audioManager)
        self.maintManager = MaintManager(game,self.manager)
    def loadTheme(self,themePath):
        self.manager.get_theme().load_theme(themePath)
    
    def update(self):
        self.settingsUI.update()

    def processEvents(self,event,audioManager,world):
        self.projectUIWrapper.processEvent(event,self.waterManager)
        self.turnBar.processEvents(event,self,audioManager)
        self.settingsUI.processEvent(event)
        self.explainUI.processEvent(event)