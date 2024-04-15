import pygame 
from pygame import Rect

import pygame_gui

from pygame_gui.elements import UIButton
from pygame_gui.core import ObjectID
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_progress_bar import UIProgressBar
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.elements.ui_scrolling_container import UIScrollingContainer

from .statisticsUI import StatisticsWindow
from .projectsUI import ProjectsUI
from .notificationsBoxUI import NotificationsBoxUI
from .turnBarUI import TurnBarUI

def createId(txt):
    return ObjectID(class_id="@"+txt,object_id="#"+txt)


class MainGameUI:
    def __init__(self,manager,themePath,world,game):
        #have to create manager correctly
        self.manager = manager
        self.loadTheme(themePath)
        self.statsWindowWrapper = StatisticsWindow(manager)
        self.turnBar = TurnBarUI(manager)
        self.notificationBox = NotificationsBoxUI(manager)
        self.projectUIWrapper = ProjectsUI(manager,self.statsWindowWrapper.statsWindow,self.notificationBox)
        self.projectUIWrapper.setWorld(world)
        self.projectUIWrapper.setGame(game)
    def loadTheme(self,themePath):
        self.manager.get_theme().load_theme(themePath)
    
    def processEvents(self,event):
        self.projectUIWrapper.processEvent(event)
        self.turnBar.processEvents(event)