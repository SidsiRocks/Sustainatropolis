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

text = """"""

def createId(txt):
    return ObjectID(class_id="@"+"NotificationsBox",object_id="#"+txt)

class NotificationsBoxUI:
    def __init__(self,manager):
        self.money = 10000
        self.txtBox,self.moneyButton = self.createNotificationBox(manager)
        
    def setMoney(self,curMoney):
        self.money = curMoney
        self.moneyButton.set_text(f"Money: {self.money}")
    def diffMoney(self,incMoney):
        self.money += incMoney
        self.moneyButton.set_text(f"Money: {self.money}")
    def createNotificationBox(self,manager):
        topPad = 10
        leftPad = 10
        width = 300
        height = 500 
        txtBoxRect = Rect(leftPad,topPad,width,height)
        txtBox = UITextBox(html_text= text,
            relative_rect=txtBoxRect,
            manager=manager,
            object_id=createId("notifications Box"))

        currencyWidth = 200
        currenctHeight = 80
        currencyRect = Rect(leftPad,txtBoxRect.top + height + topPad,currencyWidth,currenctHeight)
        currentMoney = UIButton(relative_rect=currencyRect,
            text=f"Money: {self.money}",manager=manager,
            object_id=createId("currencyButton"))
        return txtBox,currentMoney
    
    def clearHtmlText(self):
        self.txtBox.set_text("")
    def appendHtmlText(self,text):
        self.txtBox.append_html_text(text)