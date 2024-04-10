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

#modifing ovject id to be common so styling can be done together
def createObjectId(txt):
    return "#"+txt
def getTxtFromObjectId(objId):
    return objId[1:]
def createClassId(txt):
    return "@"+txt
def getTxtFromClassId(classId):
    return classId[1:]
def createId(txt):
    return ObjectID(class_id=createClassId(txt),object_id=createObjectId(txt))

def extractMainObjectId(objId):
    for i in range(len(objId)-1,-1,-1):
        if objId[i] == '.':
            return objId[i+1:]
    return objId
class ProjectsUI:
    def __init__(self,manager,statsWindow):
        self.projectLst = ["waterTreatment","sewagePlant","waterPump",
                           "purificationPlant","industrialPlant","solarPower",
                           "powerPlant","windMill"]
        self.projectNameButtonDct = {}
        self.projectListWindow = self.createProjectsList(statsWindow,manager)
        self.externalEventListener = None
    def createProjectButton(self,projLstWinScroll,x,projName,manager):
        imgBtnWidth = 150
        #imgBtnHt for these values is 175
        imgBtnPadX = 10
        imgBtnPady = 10

        x += imgBtnPadX

        projLstHeight = projLstWinScroll.rect.height
        imgBtnHt = projLstHeight - 4 * imgBtnPady
        print("image button height is:",imgBtnHt)
        projLstRect = Rect(x,imgBtnPadX,imgBtnWidth,imgBtnHt)

        curBut = UIButton(relative_rect=
            projLstRect,text="",
            manager=manager,container=projLstWinScroll,
            object_id=ObjectID(class_id='@projectButtons',
            object_id='#'+projName) )

        x += imgBtnWidth
        return (x,curBut)

    def createProjectsList(self,statsWindow,manager):
        projectListWidth = 1200
        projectListHeight = 250
        padX = 10
        padY = 10

        statsWindowRect = statsWindow.rect
        statWinWidth = statsWindowRect.width
        statWinBottomRight = statsWindowRect.bottomright
        windowHeight = manager.window_resolution[1]

        projectListLeft = statWinBottomRight[0] - statWinWidth - padX - projectListWidth
        projectsListTop = windowHeight - padY - projectListHeight

        projectsListRect = Rect(projectListLeft,projectsListTop,projectListWidth,projectListHeight)
        projectListWindow = UIWindow(rect=projectsListRect,manager=manager,
            window_display_title="Projects List",
            object_id=createId("projectsList"),
            resizable=False,draggable=False)

        compensateScrollBarHeight = 35
        projectListScrollableRect = Rect(0,0,projectListWidth,projectListHeight - compensateScrollBarHeight)    
        projectListScrollable = UIScrollingContainer(relative_rect=projectListScrollableRect,manager=manager,
            container=projectListWindow,object_id=createId("projectScrollingContainer"))

        x = 0
        for name in self.projectLst:
            (z,curBtn) = self.createProjectButton(projectListScrollable,x,name,manager)
            x = z
            self.projectNameButtonDct[name] = curBtn

        #set scrollable window size here will be different
        #doesnt seem to be working either
        projectListScrollable.set_scrollable_area_dimensions((x,projectListScrollableRect.height))
        return projectListWindow
    def setExtEventListener(self,extEventLst):
        self.externalEventListener = extEventLst
    def processEvent(self,event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            buttonName = getTxtFromObjectId(extractMainObjectId(event.ui_object_id))
            if buttonName in self.projectNameButtonDct:
                if self.externalEventListener:
                    self.externalEventListener(buttonName)
    
    