from pygame import Rect
from .maintenanceBarUI import MaintanaceBarUI
class Project:
    #see how to get manager here to create the UI
    def __init__(self,tile,tileName,pos,offsetFromProj,manager,mode="normal",createMainBar = True,maint=100):
        self.tile = tile
        self.mode = mode 
        self.pos = pos
        #currently offset from proj (0,0) but would come from
        #a dictionary in general
        self.maintBar = None
        self.maintenance = maint
        self.tileName = tileName
        if createMainBar and mode=="normal":
            self.maintBar = MaintanaceBarUI(self.pos,
                                relative_rect=Rect(0,0,100,30),
                                manager=manager,offsetFromProj=offsetFromProj,
                                current_progress=self.maintenance)

    def updateMaintBar(self,cameraOffset):
        if self.maintBar != None:
            self.maintBar.updateOffsetPos(cameraOffset)
    
    def decMaintenance(self,dec):
        if self.maintenance - dec < 0:
            self.maintenance = 0
        else :
            self.maintenance = self.maintenance - dec 
        self.maintBar.set_current_progress(self.maintenance)
    def setMaintenacne(self,maint):
        self.maintenance = maint 
        self.maintBar.set_current_progress(self.maintenance)