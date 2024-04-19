import pygame

from pygame_gui.core import ObjectID
from typing import Union, Tuple, Optional
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui import UI_BUTTON_PRESSED
from .MessageWindow import MessageWindow

def emptyFunc():
    pass

class OnDismissCallFunc(MessageWindow):
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
                 onCloseFunc = emptyFunc,buttonMsg:str = "Dismiss",
                 onCloseButtonFunc = emptyFunc):

        super().__init__(rect,html_message,
                        buttonHt,buttonWidth,
                        paddingY,paddingX,manager,
                        window_display_title,object_id,
                        visible,buttonMsg=buttonMsg)
        self.onCloseFunc = onCloseFunc
        self.onCLoseButtonFunc = onCloseButtonFunc

    def kill(self):
        super().kill()

    def process_event(self, event: pygame.event.Event) -> bool:
        """
        Process any events relevant to the message window. In this case we just close the window
        when the dismiss button is pressed.

        :param event: a pygame.Event.

        :return: Return True if we 'consumed' this event and don't want to pass it on to the rest
                 of the UI.

        """
        consumed_event = super().process_event(event)

        if event.type == UI_BUTTON_PRESSED and event.ui_element == self.dismissButton:
            self.onCloseFunc()
            self.kill()
        return consumed_event
    
    def on_close_window_button_pressed(self):
        self.onCLoseButtonFunc()
        self.kill()