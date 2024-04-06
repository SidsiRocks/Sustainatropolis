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


def createId(txt):
    return ObjectID(class_id="@"+txt,object_id="#"+txt)

class TurnBarUI:
    def __init__(self,manager):
        (self.strtYrLbl,self.endYrLbl,self.crntYrLbl,self.turnBar) = self.createTurnBar(manager)

    def createTurnBar(self,manager):
        width = manager.window_resolution[0]
        height = manager.window_resolution[1]

        turnBarWidth = 200
        turnBarHeight = 20
        txtLblWidth  = 100 
        txtLblHeight = 30

        strtLblTxt  = "2020"
        endLblTxt = "2040"
        crntLblTxt = "2030"

        prgrsBarRect = Rect((width-turnBarWidth)//2,0,turnBarWidth,turnBarHeight)
        prgrsBarLeft = prgrsBarRect.left
        prgrsBarRight = prgrsBarLeft + turnBarWidth
        prgrsBarBottom = turnBarHeight
        startYearLblRect = Rect(prgrsBarLeft-txtLblWidth,0,txtLblWidth,txtLblHeight)
        endYearLblRect = Rect(prgrsBarRight,0,txtLblWidth,txtLblHeight)
        crntYearLblRect = Rect((width-txtLblWidth)/2,prgrsBarBottom,txtLblWidth,txtLblHeight,text=strtLblTxt)

        turnBar = UIProgressBar(
            relative_rect=prgrsBarRect,manager=manager,
            object_id=createId("Number Turn Progress")
        )

        strtYrLbl = UILabel(relative_rect=startYearLblRect,manager=manager,text=strtLblTxt)
        endYrLbl = UILabel(relative_rect=endYearLblRect,manager=manager,text=endLblTxt)
        crntYrLbl = UILabel(relative_rect=crntYearLblRect,manager=manager,text=crntLblTxt)

        return (strtYrLbl,endYrLbl,crntYrLbl,turnBar)