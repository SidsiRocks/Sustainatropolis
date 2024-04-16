import pygame as pg
from .gameWorldAlt import GameData
from .util import isoCoordToRenderPos
class GroundRender:
    def __init__(self,camera,groundBuffSize,centerOffset,imageOffset,gameData:GameData):
        self.groundBuffSize = groundBuffSize
        self.centerOffset = centerOffset
        self.groundSurface = pg.Surface(self.groundBuffSize).convert_alpha()
        self.firstRender = True
        self.gameData = gameData
        self.groundCenterOffset = centerOffset
        self.imageOffset = imageOffset #
        self.camera = camera
    def drawToGroundBuff(self):
        groundImgArr = self.gameData.imgArr
        groundData = self.gameData.groundData
        centerOffset = self.centerOffset
        
        for x in range(self.gameData.noBlockX):
            for y in range(self.gameData.noBlockY-1,-1,-1):
                renderPos = isoCoordToRenderPos((x,y),centerOffset)
                curImg = groundImgArr[groundData[x][y]["tile"]]
                #print("x:",x,"y:",y,"renderPos:",renderPos)
                self.groundSurface.blit(curImg,renderPos)
    def drawGround(self,screen):
        if self.firstRender:
            self.drawToGroundBuff()
            self.firstRender = False
        screen.blit(self.groundSurface,
                    (self.imageOffset[0]-self.camera.getX(),
                    self.imageOffset[1]-self.camera.getY()))