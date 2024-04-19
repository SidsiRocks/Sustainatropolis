from pygame_gui.elements import UIButton
from pygame import Rect
from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements.ui_image import UIImage

from .util import ldImage

import pygame_gui
import json

from .hideOnCloseWindow import HideUIwindow

class ExplanationUI:
    def __init__(self,manager:IUIManagerInterface):
        self.mainWindow = (1200,771)

        width = manager.window_resolution[0]
        height = manager.window_resolution[1]

        explainButtonWidth  = 80
        explainButtonHeight = 80
        padX = 10

        mainExplainWinRect = Rect((width-self.mainWindow[0])/2,
                                  (height-self.mainWindow[1])/2
                                  ,self.mainWindow[0],self.mainWindow[1])
        #have to remove window padding in styling and add ObjectID
        self.mainExplainWin = HideUIwindow(mainExplainWinRect,manager,"",
                                       resizable=False,draggable=False,
                                       object_id=ObjectID("#explainWin","@explainWin"),
                                       visible=0)

        imgPadY = 100
        buttonHeight = mainExplainWinRect.height -imgPadY
        buttonWidth = mainExplainWinRect.width

        miscImagesDict = json.load(open("res/json/miscImages.json"))
        explainImg = ldImage(miscImagesDict["ExplanationImg"])

        self.img = UIImage(Rect(0,0,buttonWidth,buttonHeight),image_surface=explainImg,
                           manager=manager,container=self.mainExplainWin,
                           object_id=ObjectID("#explainImg","@explainImg"))

        explainBtnRect = Rect(width-2*explainButtonWidth-padX,0,explainButtonWidth,explainButtonHeight)
        self.explainButton = UIButton(explainBtnRect,text="",
                                  manager=manager,
                                  object_id=ObjectID("#explainBtn","@explainBtn"),starting_height=2)
    
    def processEvent(self,event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            objectID = event.ui_object_id
            if objectID == "#explainBtn":
                self.mainExplainWin.show()