import pygame
from .customUIprogress import CustomUIprogressBar
from pygame_gui.elements.ui_world_space_health_bar import UIWorldSpaceHealthBar
from .util import *
from typing import Union, Dict, Optional
from pygame import Rect
import pygame
from pygame_gui.elements.ui_progress_bar import UIProgressBar
from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface
from pygame_gui.core import UIElement
from pygame_gui.elements.ui_status_bar import UIStatusBar

class MaintanaceBarUI(CustomUIprogressBar):
    #def __init__(self,isoPos,offsetFromProj):
    def __init__(self,isoPos,offsetFromProj,
                 relative_rect: pygame.Rect,
                 manager: Optional[IUIManagerInterface] = None,
                 container: Optional[IContainerLikeInterface] = None,
                 parent_element: Optional[UIElement] = None,
                 object_id: Optional[Union[ObjectID,str,]] = None,
                 anchors: Optional[Dict[str,Union[str,UIElement]]] = None,
                 visible:int = 1,current_progress:float = 0,maximum_progress:float = 100.0,
                 projName = ""):
        super().__init__(relative_rect=relative_rect,
                         manager=manager,
                         container=container,
                         parent_element=parent_element,
                         object_id=object_id,
                         anchors=anchors,
                         visible=visible,
                         current_progress=current_progress,
                         maximum_progess=maximum_progress,projName=projName)
        self.isoPos = isoPos
        self.offsetFromProj = offsetFromProj
        #self.status_changed variable is relevant
        self.isoRenderPos = isoCoordToRenderPos(self.isoPos,(0,0))
        self.pos = self.isoRenderPos
        self.posChanged = False
    @property
    def position(self):
        return self.pos
    def updateOffsetPos(self,cameraOffset):
        newPos = (self.isoRenderPos[0] +cameraOffset[0] ,self.isoRenderPos[1] + cameraOffset[1])
        if newPos != self.pos:
            #print("Position changed")
            self.pos = newPos
            self.posChanged = True
    def update(self,time_delta:float):
        super().update(time_delta)
        if self.alive():
            if self.posChanged:
                self.set_relative_position(self.pos)   
                self.posChanged = False