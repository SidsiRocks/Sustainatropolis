import pygame 
import json
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
        #order also important
        self.projectLst,self.projectToCostMap = self.loadProjectLstAndCost("game/projectCostData.json")
        self.projectNameButtonDct = {}
        self.projectListWindow = self.createProjectsList(statsWindow,manager)
        self.currentProject = None
        self.world = None
        self.projectListRect = None
        #this will be read from and rednered to in game
        self.curTileDrawReq = {}
    def loadProjectLstAndCost(self,jsonFilePath):
        data = json.load(open(jsonFilePath))
        projectLst = data["projectLists"]
        projectToCostMap = data["projectToCostMap"] 
        return projectLst,projectToCostMap       
    def createCurrencyButton(self,projButton,projButRect:Rect,projName,manager,projLstWinScroll):
        width = 30
        height = 30
        buttonWdth = projButRect.width 
        buttonHt = projButRect.height
        offX = -10
        offY = -10
        currencyRect = Rect(projButRect.left + buttonWdth - width + offX,
                            projButRect.top + buttonHt - height + offY,
                            width,height)
        currencyLbl = UILabel(relative_rect=currencyRect,text=str(self.projectToCostMap[projName]),
            object_id=ObjectID(
            object_id="#"+projName+"Currency",
            class_id="@currencyButton")
            ,manager=manager,container=projLstWinScroll)
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
        self.createCurrencyButton(curBut,projLstRect,projName,manager,projLstWinScroll)

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
        self.projectListRect = projectsListRect
        print("created project list rect" , projectsListRect , self.projectListRect)
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
    def clickedOnWorld(self,x,y):
        #may want to add something to cancel placement like left clicking
        if self.currentProject != None and self.world.checkPlacementValid(x,y,self.currentProject):
            self.world.placeObject(x,y,self.currentProject)
            self.currentProject = None
        else :
            print(self.currentProject)
    def hoverOnWorld(self,x,y):
        if self.currentProject != None:
            if self.world.checkPlacementValid(x,y,self.currentProject):
                self.curTileDrawReq = {"tile":self.currentProject,"pos":(x,y),"mode":"transparent"}
            else:
                self.curTileDrawReq = {"tile":self.currentProject,"pos":(x,y),"mode":"red"}
        # else :
        # else : 
                # self.curTileDrawReq = None
    def processEvent(self,event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            print("inside processEvents button pressed")
            buttonName = getTxtFromObjectId(extractMainObjectId(event.ui_object_id))
            print(buttonName)
            if buttonName in self.projectNameButtonDct:
                self.handleProjectButtonClick(buttonName)
    def handleProjectButtonClick(self,buttonName):
        print("inside handleProjectButtonClick" , buttonName , self.currentProject)
        if self.currentProject != None and self.currentProject == buttonName:
            self.currentProject = None
            # self.hoverOnWorld(-1,-1)
        else :
            self.currentProject = buttonName
    def setWorld(self,world):
        self.world = world