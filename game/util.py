import pygame as pg
from .settings import TILE_SIZE
size = 20
def ldImage(imgPath):
    return pg.image.load(imgPath).convert_alpha()

font = None
def drawDebugText(screen,text,colour,pos):
    global font 
    if font == None:
        font = pg.font.SysFont(None,size)

    txtImg = font.render(text,True,colour)
    txtBoundBox = txtImg.get_rect(topleft=pos)
    #print("drawing text here text is:",text,"colour is:",colour,"pos is:",pos)
    screen.blit(txtImg,txtBoundBox)            

def isoCoordToRenderPos(posXY,centreOffset):
    x = posXY[0]
    y = posXY[1]
    renderX = (x+y)*TILE_SIZE
    renderY = ((x-y)*TILE_SIZE)/2
    return (renderX+centreOffset[0],renderY+centreOffset[1])

def isoRenderPosToImgRenderPos(posXY,imgWdth,imgHt):
    newX = posXY[0] + TILE_SIZE - imgWdth/2
    newY = posXY[1] + TILE_SIZE - imgHt
    return (newX,newY)
