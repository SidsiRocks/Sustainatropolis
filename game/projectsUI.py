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
from pygame_gui.windows.ui_message_window import UIMessageWindow

from .statisticsUI import StatisticsWindow
from .MessageWindow import MessageWindow
from .powerManagement import PowerManagement

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
    def __init__(self,manager,statsWindow,game,notificationBox):
        #order also important
        self.projectLst,self.projectToCostMap = self.loadProjectLstAndCost("res/json/projectCostData.json")
        self.projectNameButtonDct = {}
        self.projectListWindow = self.createProjectsList(statsWindow,manager)
        self.currentProject = None

        self.notificationBox = notificationBox
        #this will be read from and rednered to in game
        self.curTileDrawReq = {}
        self.manager = manager
        self.game = game
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
    def createProjectLabel(self,labelWidth,labelTxt,projLstWinScroll,projButtonRect,manager):
        labelHeight = 30
        padY = 10
        labelRect = Rect(projButtonRect.left,projButtonRect.top + padY,labelWidth,labelHeight)
        curLabl = UILabel(relative_rect=labelRect,text=labelTxt,manager=manager,container=projLstWinScroll,object_id=ObjectID("#"+labelTxt+"Lbl","@projectDescLbl"))
        return curLabl
    def createProjectButton(self,projLstWinScroll,x,projName,manager):
        imgBtnWidth = 170
        #imgBtnHt for these values is 175
        imgBtnPadX = 10
        imgBtnPady = 10

        x += imgBtnPadX

        projLstHeight = projLstWinScroll.rect.height
        imgBtnHt = projLstHeight - 4 * imgBtnPady
        projLstRect = Rect(x,imgBtnPadX,imgBtnWidth,imgBtnHt)

        curBut = UIButton(relative_rect=
            projLstRect,text="",
            manager=manager,container=projLstWinScroll,
            object_id=ObjectID(class_id='@projectButtons',
            object_id='#'+projName) )
        self.createCurrencyButton(curBut,projLstRect,projName,manager,projLstWinScroll)
        self.createProjectLabel(imgBtnWidth,projName,projLstWinScroll,projLstRect,manager)

        x += imgBtnWidth
        return (x,curBut)

    def createProjectsList(self,statsWindow,manager):
        projectListWidth = 1200
        projectListHeight = 290
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
        if self.currentProject != None and self.game.world.checkPlacementValid(x,y,self.currentProject):
            self.notificationBox.diffMoney(-self.projectToCostMap[self.currentProject])
            self.game.world.placeObject(x,y,self.currentProject)
            oldProjName = self.currentProject
            self.currentProject = None
            self.curTileDrawReq = {}
            return oldProjName
        else :
            self.currentProject = None
            self.curTileDrawReq = {}
        return None
    def hoverOnWorld(self,x,y):
        if self.currentProject != None:
            if self.game.world.checkPlacementValid(x,y,self.currentProject):
                self.curTileDrawReq = self.game.world.createProject(self.currentProject,(x,y),"transparent")
            else:
                self.curTileDrawReq = self.game.world.createProject(self.currentProject,(x,y),"red")
        # else :
        # else : 
                # self.curTileDrawReq = None
    def processEvent(self,event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            buttonName = getTxtFromObjectId(extractMainObjectId(event.ui_object_id))
            if buttonName in self.projectNameButtonDct:
                self.handleProjectButtonClick(buttonName)
    def handleProjectButtonClick(self,buttonName):
        isEnoughMoney = self.notificationBox.money >= self.projectToCostMap[buttonName]
        # isEnoughPower = self.game.powerManagement.validProjPlace(buttonName)
        # waterError = self.game.waterManagement.validProjPlace(buttonName)
        # isWaterValid = (waterError == None)

        if isEnoughMoney: 
            self.currentProject = buttonName
            
        else:
            notEnoughMoneyMsg = self.generateNotEnoughMoneyMsg(buttonName,self.notificationBox.money)
            self.createNotEnoughWindow(notEnoughMoneyMsg)
        # print(f"isEnoughPower:{isEnoughPower} for the projName:{buttonName}")
        # if self.currentProject == buttonName:
            # self.currentProject = None
            # self.curTileDrawReq = {}
        # elif isEnoughMoney and isEnoughPower and isWaterValid:
            # self.currentProject = buttonName
        # elif not isEnoughMoney:
        #     notEnghMoneyMsg = self.generateNotEnoughMoneyMsg(buttonName,self.notificationBox.money)
        #     self.createNotEnoughWindow(notEnghMoneyMsg)
        # elif not isEnoughPower:
        #     notEnghPowerMsg = self.generateNotEnoughPowerMsg(buttonName,self.game.powerManagement)
        #     self.createNotEnoughWindow(notEnghPowerMsg)
        # elif waterError != None:
        #     incrWaterErrorMsg = self.generateWaterErrorMsg(buttonName,waterError)
        #     self.createNotEnoughWindow(incrWaterErrorMsg)
    #should create one and reload as needed possibly
    #also need to deactivate remaining components in the mean time
    def generateWaterErrorMsg(self,projName,waterError):
        typeOfError = waterError[0]
        waterVal1 = waterError[1][0]
        waterVal2 = waterError[1][1]
        txt = f"""<font face='Montseraat' color="#ffffff">
Require {typeOfError} of quantity:{waterVal2} to build
{projName} but currently only have {waterVal1}</font>
"""
        return txt
    def generateNotEnoughPowerMsg(self,projName,powerManag:PowerManagement):
        projPower = powerManag.getPowerReqForProj(projName)
        totalPower = powerManag.getPowerCons() + projPower
        curPower = powerManag.getPowerProd()

        txt = f"""<font face='Montseraat' color="#ffffff">
Require power production {totalPower} to build
{projName} but currently only have {curPower}</font>
"""
        return txt
    def generateNotEnoughMoneyMsg(self,projName,curMoney):
        projCost = self.projectToCostMap[projName]
        txt = f"""<font face='Montseraat' color="#ffffff">
Require {projCost} to build
{projName} but currently only have {curMoney}</font>
        """
        return txt
    def createNotEnoughWindow(self,warnWinMessHTML):
        width = 300
        height = 300
        winWidth = self.manager.window_resolution[0]
        winHeight = self.manager.window_resolution[1]
        wanrWinRect = Rect((winWidth-width)/2,(winHeight-height)/2,width,height)
        
        buttonHt = 50
        buttonWdth = 100
        paddingY = 10
        paddingX = 15
        warnWindow = MessageWindow(wanrWinRect,warnWinMessHTML,buttonHt,
                                   buttonWdth,paddingY,paddingX,self.manager,
                                   "Not Enough Money",
                                   ObjectID(class_id="@warnWindow",object_id="#warnWindow"),1)
        return warnWindow

"""
    def createNotEnoughMoneyWindow(self,warnWinMessHTML):
        width = 500
        height = 500
        winWidth = self.manager.window_resolution[0]
        winHeight = self.manager.window_resolution[1]
        wanrWinRect = Rect((winWidth-width)/2,(winHeight-height)/2,width,height)
        warnWindow = UIMessageWindow(
            rect=wanrWinRect,
            html_message=warnWinMessHTML,
            manager=self.manager,
            window_title="Title",
            object_id=ObjectID(class_id="@warnWindow",object_id="#warnWindow")
        )
        warnWindow.dismiss_button.relative_rect.height = 50
        warnWindow.dismiss_button.relative_rect.height = 180
        warnWindow.dismiss_button.set_text("Dismiss") 
        warnWindow.set_blocking(True)
        return warnWindow
"""