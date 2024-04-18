from pygame import Rect
from .maintenanceBarUI import MaintanaceBarUI
class Project:
    #see how to get manager here to create the UI
    def __init__(self,tile,pos,offsetFromProj,manager,mode="normal",createMainBar = True):
        self.tile = tile
        self.mode = mode 
        self.pos = pos
        #currently offset from proj (0,0) but would come from
        #a dictionary in general
        self.maintBar = None
        if createMainBar and mode=="normal":
            self.maintBar = MaintanaceBarUI(self.pos,
                                relative_rect=Rect(0,0,100,30),
                                manager=manager,offsetFromProj=offsetFromProj)

    def updateMaintBar(self,cameraOffset):
        if self.maintBar != None:
            self.maintBar.updateOffsetPos(cameraOffset)
    