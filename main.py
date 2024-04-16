import pygame as pg 
from game.game import MainGameScene
from pygame.locals import *
import pygame_gui
def main():
    #flag = FULLSCREEN | DOUBLEBUF 
    flag = DOUBLEBUF
    running = True 
    playing = False 
    
    pg.init()
    pg.mixer.init()
    
    screen_width, screen_height = pg.display.Info().current_w, pg.display.Info().current_h
    screen = pg.display.set_mode((screen_width, screen_height), flag, vsync=True)

    bg_image = pg.image.load("res/graphics/imgTransparencyPlace/bg.png")
    bg_image = pg.transform.scale(bg_image,(screen_width,screen_height))

    manager = pygame_gui.UIManager((screen_width, screen_height))
    play_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((screen_width/2-100,screen_height/2-50),(200,100)),text="Play",manager=manager)


    screen = pg.display.set_mode((1200,800),flag,vsync=True)
    #screen = pg.display.set_mode((0,0),flag,vsync=True)
    clock = pg.time.Clock()

    game = MainGameScene(screen,clock)
    while running:
        # game.run()
        for event in pg.event.get() :
            if event.type == pg.QUIT:
                running = False

            manager.process_events(event)

            if event.type == pg.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:
                        playing = True
                        # game.run()
                        # manager.clear_and_reset()
                        #game.run()
        screen.blit(bg_image,(0,0))

        if playing:
            game.run()
        else:
            manager.update(time_delta=clock.tick(60)/1000.0)
            manager.draw_ui(screen)
        pg.display.flip()

if __name__ == "__main__":
    main()