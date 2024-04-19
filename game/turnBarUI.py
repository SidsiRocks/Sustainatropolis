import pygame 
from pygame import Rect
import json
import shutil
from .waterManagement import WaterManagement
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.core import ObjectID
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_progress_bar import UIProgressBar
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.elements.ui_scrolling_container import UIScrollingContainer
from .highscore import HighScore
from .customUIprogress import CustomUIprogressBar
from .onCloseButtonEvent import OnCloseWindowButton

def createId(txt):
    return ObjectID(class_id="@"+txt,object_id="#"+txt)
def createProgressId(txt):
    return ObjectID(class_id="@"+"TurnProgress",object_id="#"+txt)
def createStartEndLabelId(txt):
    return ObjectID(class_id="@"+"TurnStartEndLabel",object_id="#"+txt)
def createCurrentYearLabel(txt):
    return ObjectID(class_id="@"+"TurnCurrentYearLabel",object_id="#"+txt)
class TurnBarUI:
    def __init__(self,manager,game,turnBarFilePath):
        self.game = game
        self.strtYr = 2020
        self.crntYr = 2020
        self.endYr = 2040
        self.moneyPerYear = 20
        self.readTurnBarUI(filePath=turnBarFilePath)
        self.waterManagementManager = self.game.waterManagement
        (self.crntYrLbl,self.turnBar,self.nextTurnButton,self.scoreLbl) = self.createTurnBar(manager)
        self.notifMessages = json.load(open("res/json/notifMessages.json"))

        
        self.highscore_db = HighScore()
        # self.processEvents(None,None,None)
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
        crntLblTxt = str(2020 + (self.crntYr-2017)//4)

        prgrsBarRect = Rect((width-turnBarWidth)//2,0,turnBarWidth,turnBarHeight)
        prgrsBarLeft = prgrsBarRect.left
        prgrsBarRight = prgrsBarLeft + turnBarWidth
        prgrsBarBottom = turnBarHeight

        startYearLblRect = Rect(prgrsBarLeft-txtLblWidth,0,txtLblWidth,txtLblHeight)
        endYearLblRect = Rect(prgrsBarRight,0,txtLblWidth,txtLblHeight)
        crntYearLblRect = Rect((width-txtLblWidth)/2,prgrsBarBottom,txtLblWidth,txtLblHeight)

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

        # strtYrLbl = UILabel(relative_rect=startYearLblRect,manager=manager,text=strtLblTxt,object_id=createStartEndLabelId("startYrLbl"))
        # endYrLbl = UILabel(relative_rect=endYearLblRect,manager=manager,text=endLblTxt,object_id=createStartEndLabelId("endYrLbl"))
        crntYrLbl = UILabel(relative_rect=crntYearLblRect,manager=manager,text=crntLblTxt,object_id=createStartEndLabelId("curYrLbl"))

        nextTurnButton = UIButton(relative_rect=nextTurnButtonRects,manager=manager,
                                  text="Next Turn",
                                  object_id=ObjectID(object_id="#nextTurnButton",class_id="@nextTurnButton"),starting_height= 2)

        nextTurnXmid = nextTurnButtonRects.left + nextTurnButtonRects.width/2
        nextTurnXbottom = nextTurnButtonRects.top + nextTurnButtonRects.height

        scoreLblWidth = 180
        scoreLblHeight = 40
        scoreLblRect = Rect(nextTurnXmid - scoreLblWidth/2,nextTurnXbottom,scoreLblWidth,scoreLblHeight)
        scoreLbl = UILabel(relative_rect=scoreLblRect,text="0",object_id=ObjectID("@scoreLbl","#scoreLbl"),manager=self.game.manager)

        return (crntYrLbl,turnBar,nextTurnButton,scoreLbl)

    def setScore(self,scoreNum):
        self.scoreLbl.set_text(str(scoreNum))

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
        if crntYr <= self.endYr:
            self.crntYr = crntYr
            self.crntYrLbl.set_text(str(2020 + (crntYr-2017)//4))
            self.updatePrgrsBar()
        else:
            self.generateGameOverWindow()
    
    def handleGameExit(self):
        self.game.stopPlaying()
        shutil.copyfile("game/defaultStartGameData/mapData.json","game/currentStartGame/mapData.json")
        shutil.copyfile("game/defaultStartGameData/money.txt","game/currentStartGame/money.txt")
        shutil.copyfile("game/defaultStartGameData/turnBarYear.txt","game/currentStartGame/turnBarYear.txt")
        shutil.copyfile("game/defaultStartGameData/writeMaint.txt","game/currentStartGame/writeMaint.txt")

    def generateGameOverWindow(self):
        onFuncButtonClose = lambda: self.handleGameExit()
        closeWindowWidth = 400
        closeWindowHeight = 400
        gameOverRect = Rect((self.game.width-closeWindowWidth)/2,
                            (self.game.height - closeWindowHeight)/2,
                            closeWindowWidth,closeWindowHeight)
        
        score = self.game.waterManagement.score
        gameOverTxt=f"""<font face='Montserrat' color="#ffffff" size=4.5>Game Over You had a final score of {score} </font>"""
        gameOverWindow = OnCloseWindowButton(rect=gameOverRect,
                            html_message=gameOverTxt,buttonHt=100,
                            buttonWidth=80,paddingY=10,paddingX=10,
                            manager=self.game.manager,
                            window_display_title="Game Over",
                            object_id=ObjectID("@gameOverWindow","#gameOverWindow"),
                            resizable=False,draggable=False,onCloseFunc=onFuncButtonClose)
        gameOverWindow.set_blocking(True)
        
    def createNotifMessage(self,year,message , title):
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
        ans += "<font face='Montserrat' color='#ffffff' size=6><b>" + title +"</b></font><br>" 
        ans += "<div style='text-align: right; font-size: 4; color: #ffffff;'>"+season+", " + str(2020 + (year-2017)//4) +   "</div>"
        ans += "<font face='Montserrat' color='#ffffff' size=6><b>---------------------------</b></font>"
        ans += "<font face='Montserrat' color='#f0f0f0' size=4>"+message+"</font>"
        ans += "<font face='Montserrat' color='#ffffff' size=6><b>---------------------------</b></font>"



        return ans 

    def proceedEvent(self,event_name,maingameui) :
        if event_name != "Welcome" :
            self.waterManagementManager.processNotifs(event_name)
        maingameui.notificationBox.appendHtmlText(self.createNotifMessage(self.crntYr,self.notifMessages[event_name],self.notifMessages["Titles"][event_name]))


    def processEvents(self,event,maingameui,audioManager):
        if   event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.nextTurnButton:
            if self.crntYr < self.endYr+1:
                self.waterManagementManager.processNotifs("Reset")
                self.waterManagementManager.decreaseMaintenance()
                self.setCrntYear(self.crntYr+1)
                audioManager.playSound("celebration")
                print("Current Year is", self.crntYr)
                if self.crntYr == 2021 :  #summer
                    maingameui.notificationBox.clearHtmlText()
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
                    maingameui.notificationBox.clearHtmlText()
                    self.proceedEvent("Drought",maingameui)                                   
                    self.proceedEvent("Holi",maingameui)                                   
                elif self.crntYr == 2026 : #Rainy
                    self.proceedEvent("Rainy",maingameui)
                elif self.crntYr == 2027 : #Autumn
                    self.proceedEvent("Tourists",maingameui)
                elif self.crntYr == 2028 : #Winter
                    self.proceedEvent("DamRelease",maingameui)
                elif self.crntYr == 2029 : #Summer
                    maingameui.notificationBox.clearHtmlText()
                    self.proceedEvent("Summer",maingameui)
                elif self.crntYr == 2030 : #Rainy
                    self.proceedEvent("LessRain",maingameui)
                elif self.crntYr == 2031 :  #Autumn
                    self.proceedEvent("InfraExp",maingameui)
                elif self.crntYr == 2032 :  #Winter
                    self.proceedEvent("Diwali",maingameui)
                elif self.crntYr == 2033 :  #Summer
                    maingameui.notificationBox.clearHtmlText()
                    self.proceedEvent("Drought",maingameui)
                elif self.crntYr == 2034 :  #Rainy
                    self.proceedEvent("Flood",maingameui)
                elif self.crntYr == 2035 :  #Autumn
                    self.proceedEvent("Tourists",maingameui)
                elif self.crntYr == 2036 :  #Winter
                    self.proceedEvent("LessRain",maingameui)
                elif self.crntYr == 2037 :  #Summer
                    maingameui.notificationBox.clearHtmlText()
                    self.proceedEvent("Summer",maingameui)
                elif self.crntYr == 2038 :  #Rainy
                    self.proceedEvent("Rainy",maingameui)
                elif self.crntYr == 2039 : #Autumn
                    self.proceedEvent("Tourists",maingameui)
                elif self.crntYr == 2040 : #Winter 
                    self.proceedEvent("Diwali",maingameui)
                elif self.crntYr == 2041 : 
                    maingameui.notificationBox.clearHtmlText()
                    self.highscore_db.save_high_score( "Arpit" ,self.waterManagementManager.getScore())
                    scores = self.highscore_db.load_high_score()
                    for x in scores : 
                        print(x)
                    # self.highscore_db.saveScores()
                    # self.game.gameOver = True
                    # self.game.mainGameUI.explainUI.showGameOver()
                self.game.mainGameUI.notificationBox.money += self.game.waterManagement.population * 50
                self.game.mainGameUI.notificationBox.setMoney(self.game.mainGameUI.notificationBox.money)
                self.waterManagementManager.updateScore()
                self.waterManagementManager.updateVals()
                self.waterManagementManager.setStats(self.game.mainGameUI.statsWindowWrapper)

    def writeTurnBarUI(self,filePath):
        with open(filePath,'w') as turnFile:
            print(self.crntYr,file=turnFile)
            print("writing self.crntYr:",self.crntYr)
    def readTurnBarUI(self,filePath):
        data = None
        with open(filePath,"r") as turnFile:
            data = turnFile.readline()
        self.crntYr = int(data[:-1])        