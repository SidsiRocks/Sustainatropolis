import pygame as pg
from .gameWorld import GameData
from .util import drawDebugText,isoCoordToRenderPos
from .settings import TILE_SIZE
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
    __slot__ = ["screen","clock","width","height","world","playing","cameraPos","centreOffset","groundBuffSize","firstRender"]
    def __init__(self,screen,clock):
        self.screen = screen 
        self.clock = clock
        self.width,self.height = self.screen.get_size()

        self.world = GameData(50,50,self.width,self.height)
        self.playing = True

        self.cameraPos = (0,0)
        self.groundBuffSize = self.calGroundSurfaceSize()
        self.centerOffset = self.calCenterOffset(self.width,self.height)
        self.groundSurface = pg.Surface(self.groundBuffSize).convert_alpha()
        self.firstRender = True
    def run(self):
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
    def calCenterOffset(self,width,height):
        offX = -(self.world.noBlockX + self.world.noBlockY)*TILE_SIZE/2+ width/2
        offY = -(self.world.noBlockX - self.world.noBlockY)*TILE_SIZE/4 + height/2
        return (offX,offY)
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
    def drawToGroundBuff(self):
        groundImgArr = self.world.imgArr
        groundData = self.world.groundData
        centerOffset = self.calCenterOffset(self.groundBuffSize[0],self.groundBuffSize[1])
        for x in range(self.world.noBlockX):
            for y in range(self.world.noBlockY-1,-1,-1):
                renderPos = isoCoordToRenderPos((x,y),centerOffset)
                curImg = groundImgArr[groundData[x][y]["tile"]]
                #print("x:",x,"y:",y,"renderPos:",renderPos)
                self.groundSurface.blit(curImg,renderPos)
    def drawGround(self):
        imgOffsetX = (self.width - self.groundBuffSize[0])/2
        imgOffsetY = (self.height - self.groundBuffSize[1])/2
        self.screen.blit(self.groundSurface,(imgOffsetX-self.cameraPos[0],imgOffsetY-self.cameraPos[1]))
    def calGroundSurfaceSize(self):
        width  = (self.world.noBlockX + self.world.noBlockY)*TILE_SIZE
        height = ((self.world.noBlockX + self.world.noBlockY)*TILE_SIZE)//2 + 4*TILE_SIZE
        return (width,height)
    def draw(self):
        self.screen.fill((0,0,0))
        if self.firstRender:
            self.drawToGroundBuff()
            self.firstRender = False
        self.drawGround()
        fps = round(self.clock.get_fps())
        #print("fps is:",fps)
        self.drawGround()
        drawDebugText(self.screen,"fps={}".format(fps),(255,255,255),(10,10))
        pg.display.flip()