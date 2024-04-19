from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_horizontal_slider import UIHorizontalSlider
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.core import ObjectID
from pygame import Rect
from .hideOnCloseWindow import HideUIwindow
import pygame_gui

class SettingsUI:
    def __init__(self,manager,audioManager):
        self.settingsWindow,self.horizontalSlider,self.settingsButton = self.createSettingsWindow(manager)
        self.audioManager = audioManager
    def createSettingsWindow(self,manager):
        settingsWinWidth = 380
        settingsWinHeight = 200

        windowWidth = manager.window_resolution[0]
        windowHeight = manager.window_resolution[1]

        settButtonWidth  = 80
        settButtonHeight = 80
        settingsRect = Rect(windowWidth-settButtonWidth,0,settButtonWidth,settButtonHeight)
        settingsButton = UIButton(relative_rect=settingsRect,
                                  text="",manager=manager,
                                  object_id=ObjectID("#settingsButton","@settingsButton"),starting_height=2)

        settingsWinRect = Rect((windowWidth-settingsWinWidth)//2,(windowHeight-settingsWinHeight)//2,
                               settingsWinWidth,settingsWinHeight)
        settingsWindow = HideUIwindow(rect=settingsWinRect,manager=manager,
            window_display_title="Settings Window",
            object_id=ObjectID("#settingsWin","@settingsWin"),
            resizable=False,draggable=False,visible=0)
        settingsWindow.set_blocking(True)
        settingsWindow.on_close_window_button_pressed
        padY = 30
        sliderWidth = 200
        labelWidth = 100
        sliderHeight = 30
        leftPos = (settingsWinWidth-sliderWidth-labelWidth)//2
        
        labelRect = Rect(leftPos,padY,labelWidth,sliderHeight)
        sliderRect = Rect(leftPos+labelWidth,padY,sliderWidth,sliderHeight)
        horizontalSlider = UIHorizontalSlider(relative_rect=sliderRect,
                            start_value=100,value_range=(0,100),
                            manager=manager,container=settingsWindow,
                            object_id=ObjectID("#horizontalSlider","@horizontalSlider"))
        settingsLabel = UILabel(relative_rect=labelRect,text="Music Volume",manager=manager,
                                container=settingsWindow,
                                object_id=ObjectID("#settingsLabel","@settingsLabel"))
        return settingsWindow,horizontalSlider,settingsButton

    def update(self):
        sliderVal = self.horizontalSlider.get_current_value()
        self.audioManager.setVolume(sliderVal/100)
    def processEvent(self,event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            objectID = event.ui_object_id
            if objectID == "#settingsButton":
                self.settingsWindow.show()
