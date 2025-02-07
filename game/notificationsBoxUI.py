from pygame import Rect


from pygame_gui.elements import UIButton
from pygame_gui.core import ObjectID
from pygame_gui.elements.ui_text_box import UITextBox

text = """"""

def createId(txt):
    return ObjectID(class_id="@"+"NotificationsBox",object_id="#"+txt)

class NotificationsBoxUI:
    def __init__(self,manager,writeMaintFilePath):
        self.money = 8000
        self.readMoney(writeMaintFilePath)
        self.txtBox,self.moneyButton = self.createNotificationBox(manager)
    def setMoney(self,curMoney):
        self.money = curMoney
        self.moneyButton.set_text(f"Money: {self.money}")
    def diffMoney(self,incMoney):
        self.money += incMoney
        self.moneyButton.set_text(f"Money: {self.money}")
    def writeMoney(self,moneyFilePath):
        with open(moneyFilePath,"w") as moneyFile:
            print(self.money,file=moneyFile)
            print("Writing money self.money:",self.money)
    def readMoney(self,moneyFilePath):
        readMoney = 0
        with open(moneyFilePath,"r") as moneyFile:
            line = moneyFile.readline()
            print("money line is:",line)
            readMoney = line[:-1]
            self.money = int(readMoney)
    def createNotificationBox(self,manager):
        topPad = 10
        leftPad = 10
        width = 300
        height = 500 
        txtBoxRect = Rect(leftPad,topPad,width,height)
        txtBox = UITextBox(html_text= text,
            relative_rect=txtBoxRect,
            manager=manager,
            object_id=createId("notifications Box"),starting_height=2)

        currencyWidth = 250
        currenctHeight = 80
        currencyRect = Rect(leftPad,txtBoxRect.top + height + topPad,currencyWidth,currenctHeight)



        currencyTxt = f"<font face='Montserrat' color='#ffffff' size=5><b>Money:{self.money}</b></font><br>" 
        currentMoney = UIButton(relative_rect=currencyRect,
            text=f"Money: {self.money}",manager=manager,
            object_id=ObjectID("@currencyButton","#currencyButton"),starting_height=2)

        return txtBox,currentMoney
    
    def clearHtmlText(self):
        self.txtBox.set_text("")
    def appendHtmlText(self,text):
        self.txtBox.append_html_text(text)
