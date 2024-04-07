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

        print("current and maximum progress in constructor",self.current_progress,self.maximum_progress)
        
    @property
    def progress_percentage(self):
        print("current progress is:",self.current_progress,"maximum is:",self.maximum_progress)
        return self.current_progress/ self.maximum_progress
    def status_text(self):
        print("current progress is:",self.current_progress,"maximum is:",self.maximum_progress)
        return f"{self.current_progress:0.1f}/{self.maximum_progress:0.1f}"
        
    def set_current_progress(self,progress:float):
        self.current_progress = progress 
        self.percent_full = (progress*100)/self.maximum_progress