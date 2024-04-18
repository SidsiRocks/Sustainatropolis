from .util import isoCoordToRenderPos,isoRenderPosToImgRenderPos
from .Project import Project
class RockTreeRender:
    def __init__(self,camera,centerOffset,gameWorld,imgCenterOffset):
        self.camera = camera 
        self.centerOffset = centerOffset
        self.imgCenterOffset  = imgCenterOffset
        self.gameWorld = gameWorld
        self.noFrames = 0
        self.slowDown = 30

    def drawTreeRock(self,screen):
        totalCenterOffset = self.calTotalOffset()
        rockTreeData = self.gameWorld.rockTreeData
        groundImgArr = self.gameWorld.imgArr
        offsetArr = self.gameWorld.offsetArr

        for x in range(self.gameWorld.noBlockX):
            for y in range(self.gameWorld.noBlockY-1,-1,-1):
                curDict =  rockTreeData[x][y]
                if type(curDict) == Project:
                    renderPos = isoCoordToRenderPos((x,y),totalCenterOffset)
                    tileName = curDict.tile
                    curImg = groundImgArr[tileName]
                    if type(curImg) == list:
                        curImg = curImg[(self.noFrames//self.slowDown) % len(curImg)]

                    curOff = offsetArr[tileName]
                    imgRenderPos = isoRenderPosToImgRenderPos(renderPos,curImg.get_width(),curImg.get_height())
                    imgRenderPos = (imgRenderPos[0]+curOff[0],imgRenderPos[1]+curOff[1])
                    screen.blit(curImg,imgRenderPos)
        self.noFrames += 1    
        self.noFrames = self.noFrames % (9 * self.slowDown)
    def calTotalOffset(self):
        return (self.centerOffset[0]+self.imgCenterOffset[0]-self.camera.getX()
                ,self.centerOffset[1]+self.imgCenterOffset[1]-self.camera.getY())
    
    def drawPlacementReq(self,curDict,screen):
        totalCenterOffset = self.calTotalOffset()
        if curDict != {}:
            imgIndx = curDict.tile
            x,y = curDict.pos
            mode = curDict.mode
            curImg = None
            if mode == "transparent":
                curImg = self.gameWorld.transpImgArr[imgIndx]
            elif mode == "red":
                curImg = self.gameWorld.transRedArr[imgIndx]
            renderPos = isoCoordToRenderPos((x,y),totalCenterOffset)
            curOff = self.gameWorld.offsetArr[imgIndx]
            imgRenderPos = isoRenderPosToImgRenderPos(renderPos,curImg.get_width(),curImg.get_height())
            imgRenderPos = (imgRenderPos[0]+curOff[0],imgRenderPos[1]+curOff[1])
            screen.blit(curImg,imgRenderPos)
        else: 
            pass