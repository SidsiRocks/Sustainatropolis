import pygame 
from pygame import Rect
import json
from .waterManagement import WaterManagement
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.core import ObjectID
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_progress_bar import UIProgressBar
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.elements.ui_scrolling_container import UIScrollingContainer

from .customUIprogress import CustomUIprogressBar

def createId(txt):
    return ObjectID(class_id="@"+txt,object_id="#"+txt)
def createProgressId(txt):
    return ObjectID(class_id="@"+"TurnProgress",object_id="#"+txt)
def createStartEndLabelId(txt):
    return ObjectID(class_id="@"+"TurnStartEndLabel",object_id="#"+txt)
def createCurrentYearLabel(txt):
    return ObjectID(class_id="@"+"TurnCurrentYearLabel",object_id="#"+txt)
class TurnBarUI:
    def __init__(self,manager,game):
        self.game = game
        self.strtYr = 2020
        self.crntYr = 2020
        self.endYr = 2040
        self.moneyPerYear = 20
        self.waterManagementManager = self.game.waterManagement
        (self.strtYrLbl,self.endYrLbl,self.crntYrLbl,self.turnBar,self.nextTurnButton) = self.createTurnBar(manager)
        self.notifMessages = json.load(open("res/json/notifMessages.json"))
    def createTurnBar(self,manager):
        width = manager.window_resolution[0]
        height = manager.window_resolution[1]

        turnBarWidth = 250
        turnBarHeight = 40
        txtLblWidth  = 100 
        txtLblHeight = 30

        nextTurnButtonWidth  = 120
        nextTurnButtonHeight = 50

        strtLblTxt  = str(self.strtYr)
        endLblTxt = str(self.endYr)
        crntLblTxt = str(self.crntYr)

        prgrsBarRect = Rect((width-turnBarWidth)//2,0,turnBarWidth,turnBarHeight)
        prgrsBarLeft = prgrsBarRect.left
        prgrsBarRight = prgrsBarLeft + turnBarWidth
        prgrsBarBottom = turnBarHeight

        startYearLblRect = Rect(prgrsBarLeft-txtLblWidth,0,txtLblWidth,txtLblHeight)
        endYearLblRect = Rect(prgrsBarRight,0,txtLblWidth,txtLblHeight)
        crntYearLblRect = Rect((width-txtLblWidth)/2,prgrsBarBottom,txtLblWidth,txtLblHeight,text=strtLblTxt)

        nextTurnButtonRects = Rect((width-nextTurnButtonWidth)/2,
                                   crntYearLblRect.top + crntYearLblRect.height,
                                   nextTurnButtonWidth,nextTurnButtonHeight)

        turnBar = CustomUIprogressBar(
            relative_rect=prgrsBarRect,manager=manager,
            object_id=createProgressId("Number_Turn_Progress"),
            current_progress=(self.crntYr-self.strtYr),
            maximum_progess=(self.endYr-self.strtYr)
        )
        turnBar.set_current_progress(self.crntYr-self.strtYr)

        strtYrLbl = UILabel(relative_rect=startYearLblRect,manager=manager,text=strtLblTxt,object_id=createStartEndLabelId("startYrLbl"))
        endYrLbl = UILabel(relative_rect=endYearLblRect,manager=manager,text=endLblTxt,object_id=createStartEndLabelId("endYrLbl"))
        crntYrLbl = UILabel(relative_rect=crntYearLblRect,manager=manager,text=crntLblTxt,object_id=createStartEndLabelId("curYrLbl"))

        nextTurnButton = UIButton(relative_rect=nextTurnButtonRects,manager=manager,
                                  text="Next Turn",
                                  object_id=ObjectID(object_id="#nextTurnButton",class_id="@nextTurnButton"))

        return (strtYrLbl,endYrLbl,crntYrLbl,turnBar,nextTurnButton)

    def updatePrgrsBar(self):
        self.turnBar.set_current_progress(self.crntYr-self.strtYr)
        self.turnBar.current_progress = self.crntYr - self.strtYr

    def setStartYear(self,strtYr):
        self.strtYr = strtYr
        self.strtYrLbl.set_text(str(strtYr))
        self.updatePrgrsBar()
    def setEndYear(self,endYr):
        self.endYr = endYr
        self.endYrLbl.set_text(str(endYr))
        self.updatePrgrsBar()
    def setCrntYear(self,crntYr):
        self.crntYr = crntYr
        self.crntYrLbl.set_text(str(crntYr))
        self.updatePrgrsBar()

    def createNotifMessage(self,year,message):
        season = ""
        if year%4==1 : 
            season = "Summer"
        elif year%4 == 2 :
            season = "Rainy"
        elif year%4 == 3 :
            season = "Autumn"
        else:
            season = "Winter"
        ans = ""
        ans += "<font face='Montserrat' color='#ffffff' size=6><b>"+season+", " + str(2020 + (year+1-2020)//5) +   "</b></font>"
        ans += "<font face='Montserrat' color='#ffffff' size=6><b>---------------------------</b></font>"
        ans += "<font face='Montserrat' color='#f0f0f0' size=4>"+message+"</font>"
        ans += "<font face='Montserrat' color='#ffffff' size=6><b>---------------------------</b></font>"

        return ans 

    def proceedEvent(self,event_name,maingameui) : 
        self.waterManagementManager.processNotifs(event_name)
        maingameui.notificationBox.appendHtmlText(self.createNotifMessage(self.crntYr,self.notifMessages[event_name]))


    def processEvents(self,event,maingameui,audioManager):
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.nextTurnButton:
            if self.crntYr < self.endYr:
                self.waterManagementManager.processNotifs("Reset")
                self.setCrntYear(self.crntYr+1)
                audioManager.playSound("celebration")
                if self.crntYr == 2021 :  #summer
                    self.proceedEvent("Summer",maingameui)
                    self.proceedEvent("Holi",maingameui)
                elif self.crntYr == 2022 : #Rainy
                    self.proceedEvent("Flood",maingameui)                 
                elif self.crntYr == 2023 : #Autumn
                    self.proceedEvent("Tourists",maingameui) 
                    self.proceedEvent("DamRelease",maingameui)
                elif self.crntYr == 2024 : #Winter          
                    self.proceedEvent("Diwali",maingameui)   
                elif self.crntYr == 2025 : #Summer
                    self.proceedEvent("Drought",maingameui)                                   
                    self.proceedEvent("Holi",maingameui)                                   
                elif self.crntYr == 2026 : #Rainy
                    self.proceedEvent("Rain",maingameui)
                elif self.crntYr == 2027 : #Autumn
                    self.proceedEvent("Tourists",maingameui)
                elif self.crntYr == 2028 : #Winter
                    self.proceedEvent("DamRelease",maingameui)
                elif self.crntYr == 2029 : #Summer
                    self.proceedEvent("Summer",maingameui)
                elif self.crntYr == 2030 : #Rainy
                    self.proceedEvent("Rain",maingameui)
                elif self.crntYr == 2031 :  #Autumn
                    self.proceedEvent("InfraExp",maingameui)
                elif self.crntYr == 2032 :  #Winter
                    self.proceedEvent("Diwali",maingameui)
                elif self.crntYr == 2033 :  #Summer
                    self.proceedEvent("Drought",maingameui)
                elif self.crntYr == 2034 :  #Rainy
                    self.proceedEvent("Flood",maingameui)
                elif self.crntYr == 2035 :  #Autumn
                    self.proceedEvent("Tourists",maingameui)
                elif self.crntYr == 2036 :  #Winter
                    self.proceedEvent("Rain",maingameui)
                elif self.crntYr == 2037 :  #Summer
                    self.proceedEvent("Summer",maingameui)
                elif self.crntYr == 2038 :  #Rainy
                    self.proceedEvent("Rain",maingameui)
                elif self.crntYr == 2039 : #Autumn
                    self.proceedEvent("Tourists",maingameui)
                elif self.crntYr == 2040 : #Winter 
                    self.proceedEvent("Diwali",maingameui)
                self.waterManagementManager.updateVals()
                self.waterManagementManager.setStats(self.game.mainGameUI.statsWindowWrapper)
