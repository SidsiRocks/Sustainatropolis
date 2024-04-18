from typing import Union, Optional, Dict
from pygame_gui.elements import UIButton,UITextBox,UIWindow
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame import Rect
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui import UI_BUTTON_PRESSED

class MessageWindow(UIWindow):
    def __init__(self,rect:pygame.Rect,
                 html_message:str,
                 buttonHt:int,
                 buttonWdth:int,
                 paddingY:int,
                 paddingX:int,
                 manager: Optional[IUIManagerInterface] = None,
                 window_display_title:str = 'Title bar',
                 object_id:Union[ObjectID,str] = ObjectID("#message_window","@message_window"),
                 visible:int = 1):
        super().__init__(rect, manager,
                         window_display_title=window_display_title,
                         object_id=object_id,
                         resizable=True,
                         visible=visible)
        winWidth = rect.width - 30
        winHeight = rect.height - 50

        txtBoxHt = winHeight - 3*paddingY-buttonHt
        txtBoxWdth = winWidth - 2*paddingX

        txtBlockRect = Rect(paddingX,paddingY,txtBoxWdth,txtBoxHt)
        dismissButtonRect = Rect(winWidth - paddingX - buttonWdth,2*paddingY+txtBoxHt,buttonWdth,buttonHt)
        #change this appropiately
        self.dismissButton = UIButton(relative_rect=dismissButtonRect,
                                      text="Dismiss",
                                      manager=manager,
                                      container=self,
                                      object_id=ObjectID("#messageDismissButton","@messageDismissButton"),
                                      )
        #may want to add text kw args for html if want to 
        #add more html styling perhaps have to see the purpose first
        self.textBox = UITextBox(html_message,txtBlockRect,manager,container=self,
                                 object_id=ObjectID("#messageTextBox","@messageTextBox"))
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
            self.kill()

        return consumed_event