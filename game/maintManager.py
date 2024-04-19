from .onDismissCallFunc import OnDismissCallFunc
from pygame_gui.core import ObjectID
from pygame import Rect

class MaintManager:
    def __init__(self,game,manager):
        self.game = game
        self.manager = manager
        self.width = manager.window_resolution[0]
        self.height = manager.window_resolution[1]
        self.maintAllowed = True
    
    def setMaintAllowed(self,maintAllowed):
        self.maintAllowed = maintAllowed
    def handleClick(self,isoX,isoY):
        if self.maintAllowed:
            world = self.game.world
            if isoX < 0 or isoX >= self.game.world.noBlockX or isoY < 0 or isoY >= self.game.world.noBlockY:
                return
    
            rockTreeData = world.rockTreeData
            projOnLoc = rockTreeData[isoX][isoY]
            if projOnLoc == None:
                return
            if type(projOnLoc) == tuple:
                isoX,isoY = isoX+projOnLoc[0],isoY+projOnLoc[1]
                projOnLoc = rockTreeData[isoX][isoY]
            
            self.createProjectWindow(projOnLoc)
         #handle creation of maintenance window here
        
    
    def createProjectWindow(self,proj):
        projName = proj.tileName
        maint = proj.maintenance
        projMaintCost = self.game.world.projCost[proj.tileName]
        curMoney = self.game.mainGameUI.notificationBox.money

        if curMoney < projMaintCost:
            #generate not enough money error message
            self.createNotEnoughMoneyWindow(proj,projName,maint,projMaintCost,curMoney)
        else:
            if maint != 100:
                self.createMaintenanceWindow(proj,projName,maint,projMaintCost)
    def createMaintenanceWindow(self,proj,projName,maint,projMaintCost):
        text = f"""<font face='Montserrat' color="#ffffff" size=4.5>{projName} has current maintenance {maint} it would cost
{projMaintCost} to fix it</font>"""
        
        projUIWrapper = self.game.mainGameUI.projectUIWrapper
        projUIWrapper.setProjAllowed(False)
        self.setMaintAllowed(False)
        onCloseFunc = lambda: (self.fixMaintenaceFunc(proj,projMaintCost),
                               projUIWrapper.setProjAllowed(True),
                               self.setMaintAllowed(True))
        onCloseButtonFunc = lambda: (projUIWrapper.setProjAllowed(True),self.setMaintAllowed(True))

        maintWinWidth  = 400
        maintWinHeight = 400
        maintWinRect = Rect((self.width - maintWinWidth)/2,(self.height - maintWinHeight)/2,
                            maintWinWidth,maintWinHeight)
        maintWindow  = OnDismissCallFunc( maintWinRect,text,buttonHt=50,buttonWidth=100,paddingX=15,
                                          paddingY=10,window_display_title="Reapir Project",
                                          object_id= ObjectID(class_id = "@projMaintCostWindow",object_id = "#projMaintCostWindow"),
                                          resizable=False,draggable=False,manager=self.manager,
                                          onCloseFunc=onCloseFunc,buttonMsg=f"Pay {projMaintCost}",visible=1,
                                          onCloseButtonFunc=onCloseButtonFunc)
        maintWindow.set_blocking(True)
        return maintWindow

    def createNotEnoughMoneyWindow(self,proj,projName,maint,projMaintCost,curMoney):
        text = f"""<font face='Montseraat' color="#ffffff">{projName} has current maintenance {maint} it would cost
{projMaintCost} to fix it but only have {curMoney}</font>"""

        maintWinWidth  = 400
        maintWinHeight = 400
        maintWinRect = Rect((self.width - maintWinWidth)/2,(self.height - maintWinHeight)/2,
                            maintWinWidth,maintWinHeight)
        maintWindow  = OnDismissCallFunc( maintWinRect,text,buttonHt=50,buttonWidth=100,paddingX=15,
                                          paddingY=10,window_display_title="Repair Project",manager=self.manager,
                                          object_id= ObjectID(class_id = "@projMaintCostWindow",object_id = "#projMaintCostWindow"),
                                          resizable=False,draggable=False,buttonMsg=f"Pay {projMaintCost}",visible=1)
        maintWindow.set_blocking(True)
        return maintWindow

    ###Arpit add code to handle maintenance increase and decrease here
    def fixMaintenaceFunc(self,proj,projMaintCost):
        print(f"fix maintenance of function was called with {proj.tileName}")
        proj.setMaintenacne(100)
        self.game.mainGameUI.notificationBox.diffMoney(projMaintCost)
        self.game.waterManagement.upagain(proj)
        self.game.waterManagement.updateVals()