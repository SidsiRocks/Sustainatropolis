from pygame_gui.elements import UIButton
from pygame import Rect
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.core import ObjectID
from pygame_gui.elements.ui_window import UIWindow

class ExplanationUI:
    def __init__(self,manager):
        self.imgButtonSize = (150,150)
        self.explanationWinSize = (170,325)
        self.txtBoxSize = (150,150)
        
        self.explainWinPadX = (self.explanationWinSize[0]-self.imgButtonSize[0])/2
        self.explainWinPadY = (self.explanationWinSize[1]-self.imgButtonSize[1]-self.txtBoxSize[1])/3

    def makeVisible():
        pass
    def createImgButton(self,projName,enclosingWin,manager):
        padX = self.explainWinPadX
        padY = self.explainWinPadY
        buttonRect = Rect(padX,padY,self.imgButtonSize[0],self.imgButtonSize[1])
        curButton = UIButton(buttonRect,manager=manager,
                             container=enclosingWin,tool_tip_text="",
                             object_id=
                                ObjectID("#"+projName+"ExplainButton",
                                        "@"+projName+"ExplainButton"))
        return curButton
    def createTxtBox(self,explainTxt,enclosingWin,manager,projName):
        padX = self.explainWinPadX
        padY = self.explainWinPadY
        imgBtnHt = self.imgButtonSize[1]

        txtBoxRect = Rect(padX,imgBtnHt+padY,self.imgButtonSize[0],self.imgButtonSize[1])
        txtBox = UITextBox(html_text=explainTxt,
            relative_rect=txtBoxRect,manager=manager
            ,object_id=
            ObjectID("#"+projName+"ExplainTextBox"
                     ,"@"+projName+"ExplainTextBox"),container=enclosingWin)
        return txtBox
    
    def createEnclosingWin(self,projName,windowRect,manager):
        curWindow = UIWindow(rect=windowRect,manager=manager,
                    object_id=
                        ObjectID("#"+projName+"EnclosingWin",
                                 "@"+projName+"EnclosingWin"),draggable=False)

    def createMainErrorWin():
        pass