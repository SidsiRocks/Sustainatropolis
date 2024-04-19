import pygame
import pygame_gui

pygame.init()

pygame.display.set_caption('Quick Start')

windowSurface = pygame.display.set_mode((800,600))

background = pygame.Surface((800,600))
background.fill(pygame.Color("#000000"))

manager = pygame_gui.UIManager((800,600))

winRect = pygame.Rect(10,10,200,100)
uiExmplWin = pygame_gui.elements.UIWindow(
    rect=winRect,manager=manager,
    window_display_title="Test UI window",
    resizable=True)

clock = pygame.time.Clock()
isRunning = True 

buttonLayoutRect = pygame.Rect(30,20,100,20)

helloButton = pygame_gui.elements.UIButton(relative_rect=
buttonLayoutRect,text="Say Hello",
manager=manager,anchors=
{'left':'left','top':'top','bottom':'bottom','right':'right'},container=uiExmplWin) #container = specifies which container is specified

while isRunning:
    timeDelta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False 
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == helloButton:
                print("clicked on hello button")
        manager.process_events(event)
    manager.update(timeDelta)


    windowSurface.blit(background,(0,0))
    manager.draw_ui(windowSurface)

    pygame.display.update()