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

def crossProduct(v1,v2):
    return v1[0]*v2[1] - v2[0]*v1[1]

def basisVecX():
    return (TILE_SIZE,TILE_SIZE/2)
def basisVecY():
    return (-TILE_SIZE,TILE_SIZE/2)

#from statndard to isometric
def changeOfBasis(posStndrd,basisv1,basisv2):
    basisCrossProd = crossProduct(basisv1,basisv2)
    X = crossProduct(posStndrd,basisv2)/basisCrossProd
    Y = crossProduct(posStndrd,basisv1)/basisCrossProd
    return (X,Y)

def removeSpaces(txt:str):
    result = ""
    for c in txt:
        if c != ' ':
            result = result + c
    return result

def parseColour(txt:str):
    txt = removeSpaces(txt)
    if txt.startswith("rgb(") and txt.endswith(")"):
        txt = txt[4:-1]
        colorArr = [int(i) for i in txt.split(",")]
        return (colorArr[0],colorArr[1],colorArr[2])
    elif txt.startswith("rgba(") and txt.endswith(")"): 
        txt = txt[5:-1]
        colorArr = [int(i) for i in txt.split(",")]
        return (colorArr[0],colorArr[1],colorArr[2],colorArr[3])

def parseTuple(txt:str):
    txt = removeSpaces(txt)
    if txt.startswith("(") and txt.endswith(")"):
        txt = txt[1:-1]
        coordArr = [int(i) for i in txt.split(",")]
        return (coordArr[0],coordArr[1])