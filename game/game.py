import pygame as pg
from .gameWorld import GameData
import sys

def cameraMovement(width,height):
    mouse_pos = pg.mouse.get_pos()
    fractionY = 0.03 
    fractionX = 0.03
    dx = 0
    dy = 0
    speed = 25
    if mouse_pos[0] > width*(1-fractionX):
        dx = speed
    elif mouse_pos[0] < width*fractionX:
        dx = -speed
    
    if mouse_pos[1] > height*(1-fractionY):
        dy = speed
    elif mouse_pos[1] < height*fractionY:
        dy = -speed
    
    return (dx,dy)
class MainGameScene:
    __slot__ = ["screen","clock","width","height","world","playing","cameraPos"]
    def __init__(self,screen,clock):
        self.screen = screen 
        self.clock = clock
        self.width,self.height = self.screen.get_size()

        self.world = GameData(100,100,self.width,self.height)
        self.playing = True

        self.cameraPos = (0,0)

    def run(self):
        while self.playing:
            self.clock.tick(80)
            self.events()
            self.update()
            self.draw()
    def quitScene(self):
        pg.quit()
        sys.exit()
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quitScene()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quitScene()
    
    def update(self):
        (dx,dy) = cameraMovement(self.width,self.height)
        self.cameraPos = (self.cameraPos[0]+dx,self.cameraPos[1]+dy)
    def draw(self):
        self.screen.fill((0,0,0))