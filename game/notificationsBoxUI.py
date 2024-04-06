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

class NotificationsBoxUI:
    def __init__(self,manager):
        self.txtBox = self.createNotificationBox(manager)

    def createNotificationBox(self,manager):
        topPad = 10
        leftPad = 10
        width = 300
        height = 500 
        txtBoxRect = Rect(topPad,leftPad,width,height)
        txtBox = UITextBox(html_text= "<br><b>Simple test</b></br>",
            relative_rect=txtBoxRect,
            manager=manager,
            object_id=createId("notifications Box"))
        return txtBox
    
    def clearHtmlText(self):
        self.txtBox.set_text("")
    def appendHtmlText(self,text):
        self.txtBox.append_html_text(text)