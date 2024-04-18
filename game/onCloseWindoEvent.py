import pygame

from pygame_gui.core import ObjectID
from typing import Union, Tuple, Optional
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.core.interfaces import IUIManagerInterface

from .MessageWindow import MessageWindow

def emptyFunc():
    pass

class OnCloseWindow(MessageWindow):
    def __init__(self,
                 rect:pygame.Rect,
                 html_message:str,
                 buttonHt:int,
                 buttonWidth:int,
                 paddingY:int,
                 paddingX:int,
                 manager:Optional[IUIManagerInterface] = None,
                 window_display_title:str = "",
                 element_id:Optional[str] = None,
                 object_id:Optional[Union[ObjectID,str]] = None,
                 resizable: bool = False,
                 visible: int = 1,
                 draggable: bool = True,
                 onCloseFunc = emptyFunc):
        super().__init__(rect,html_message,
                        buttonHt,buttonWidth,
                        paddingY,paddingX,manager,
                        window_display_title,object_id,
                        visible)
        self.onCloseFunc = onCloseFunc
    def kill(self):
        self.onCloseFunc()
        super().kill()