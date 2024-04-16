import pygame

from pygame_gui.core import ObjectID
from typing import Union, Tuple, Optional
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.core.interfaces import IUIManagerInterface

class HideUIwindow(UIWindow):
    def __init__(self,
                 rect: pygame.Rect,
                 manager: Optional[IUIManagerInterface] = None,
                 window_display_title: str = "",
                 element_id: Optional[str] = None,
                 object_id: Optional[Union[ObjectID, str]] = None,
                 resizable: bool = False,
                 visible: int = 1,
                 draggable: bool = True):
        super().__init__(rect,manager,
                window_display_title,element_id,
                object_id,resizable,visible,
                draggable)
        self.title_bar_height = 50
        self.title_bar_close_button_width = 30
        self.title_bar = None
        self.close_window_button = None
        self.rebuild()
    def on_close_window_button_pressed(self):
        self.hide()