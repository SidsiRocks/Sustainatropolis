from typing import Union, Dict, Optional
from pygame import Rect
import pygame
from pygame_gui.elements.ui_progress_bar import UIProgressBar
from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface
from pygame_gui.core import UIElement
from pygame_gui.elements.ui_status_bar import UIStatusBar

class CustomUIprogressBar(UIStatusBar):
    element_id = "progress_bar"
    def __init__(self,
                 relative_rect: pygame.Rect,
                 manager: Optional[IUIManagerInterface] = None,
                 container: Optional[IContainerLikeInterface] = None,
                 parent_element: Optional[UIElement] = None,
                 object_id: Optional[Union[ObjectID, str, ]] = None,
                 anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
                 visible: int = 1,current_progress:float=0,maximum_progess:float=100.0):
        self.current_progress = current_progress
        self.maximum_progress = maximum_progess

        super().__init__(relative_rect=relative_rect,
                         manager=manager,
                         container=container,
                         parent_element=parent_element,
                         object_id=object_id,
                         anchors=anchors,
                         visible=visible)
        #print("current and maximum progress in constructor",self.current_progress,self.maximum_progress)
        
    @property
    def progress_percentage(self):
#        print("current progress is:",self.current_progress,"maximum is:",self.maximum_progress)
        if self.maximum_progress != 0:
            return min(self.current_progress/ self.maximum_progress,1)
        else:
            return 0
    def status_text(self):
#        print("current progress is:",self.current_progress,"maximum is:",self.maximum_progress)
        return f"{self.current_progress:0.1f}/{self.maximum_progress:0.1f}"
        
    def set_current_progress(self,progress:float):
        print("inside set current" , progress , self.current_progress)
        if self.current_progress != progress:
            self.status_changed = True
            print("status changed")
        self.current_progress = progress 
        if self.maximum_progress != 0:
            self.percent_full = min((progress*100)/self.maximum_progress,1)
        else:
            self.percent_full = 0
    def set_maximum(self,maxVal):
        print("inside set_nax" , maxVal, self.maximum_progress)
        if maxVal != self.maximum_progress:
            print("status changed in max")
            self.maximum_progress = maxVal
            self.status_changed = True 
    