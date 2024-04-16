import pygame as pg
from .gameWorldAlt import GameData
class GroundRender:
    def __init__(self,camera,groundBuffSize,centerOffset,imageOffset,gameData:GameData):
        self.groundBuffSize = groundBuffSize
        self.centerOffset = centerOffset
        self.groundSurface = pg.Surface(self.groundBuffSize).convert_alpha()
        self.firstRender = True
        self.gameData = gameData
    def drawToGroundBuff(self):
        groundImgArr = self.gameData.imgArr
        groundData = self.gameData.groundData
    def drawGround(self,screen):
        pass