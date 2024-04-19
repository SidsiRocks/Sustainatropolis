import pygame 
from pygame import Rect

import pygame_gui

from pygame_gui.elements import UIButton
from pygame_gui.core import ObjectID
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.elements.ui_scrolling_container import UIScrollingContainer

from .customUIprogress import CustomUIprogressBar

def createId(txt):
    return ObjectID(class_id="@"+txt,object_id="#"+txt)
def createLabelId(txt):
    return ObjectID(class_id="@"+"statisticsLabel",object_id="#Label_"+txt)
def createProgessLabelId(txt):
    return ObjectID(class_id="@"+"statisticalProgress",object_id="#Progress_"+txt)
class StatisticsWindow:
    def __init__(self,manager):
        self.statNames = ["Unclean Water","Clean Water","Store Water","Power Usage"]
        self.statProgressBarDict = {}
        self.statsWindow = self.createStatsWindow(manager)
        self.populateStatsWindow(manager)
    def createLabelStatBar(self,y,lblTxt,padX,padTop,
        prgrssHt,txtLblHt,statsWinWidth,manager):
        y += padTop
        txtLblRect = Rect(padX,y,statsWinWidth-5*padX,txtLblHt)
        txtLbl = UILabel(relative_rect=txtLblRect,manager=manager,
                         container=self.statsWindow,text=lblTxt,object_id=createLabelId(lblTxt))
        y += txtLblHt
        y += padTop
        prgrssRect = Rect(padX,y,statsWinWidth-5*padX,prgrssHt)
        prgrssBar = CustomUIprogressBar(
            relative_rect=prgrssRect,manager=manager,
            container=self.statsWindow,
            object_id=createProgessLabelId(lblTxt),
            current_progress=0,
            maximum_progess=0
        )
        #have to explicitly call to set progress
        prgrssBar.set_current_progress(0)
        y += prgrssHt
        return (y,txtLbl,prgrssBar)

    def setStats(self,name,curProgress,maximum=None):
        print("inside setStats",name , curProgress, maximum)
        self.statProgressBarDict[name]["progressBar"].set_current_progress(curProgress)
        if maximum!=None :
            #self.statProgressBarDict[name].maximum_progress = maximum
            self.statProgressBarDict[name]["progressBar"].set_maximum(maximum)

    def populateStatsWindow(self,manager):    
        y = 0
        padX = 10
        padTop = 10
        progressHeight = 35
        txtLblHt = 35

        statsWindowRect = self.statsWindow.rect
        statsWinWidth = statsWindowRect.width
        for stName in self.statNames:
            (z,lbl,prgrsBar) = self.createLabelStatBar(y,stName,padX,padTop,progressHeight,
                txtLblHt,statsWinWidth,manager)
            curDict = {"label":lbl,"progressBar":prgrsBar}
            y = z
            self.statProgressBarDict[stName] = curDict
        
    def createStatsWindow(self,manager):
        statsWindowRect = Rect(0,0,400,520)
        statsWindowRect.bottomright = (manager.window_resolution[0] -10,manager.window_resolution[1] -10)
        #have to ensure this window cannot be closed 
        statsWindow = UIWindow(rect=statsWindowRect,manager=manager,
        window_display_title="Statistics",
        object_id=createId("statWindow"),
        resizable=False,draggable=False)
        return statsWindow
    