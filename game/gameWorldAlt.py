from .util import ldImage,parseColour,parseTuple
from .InvalidPlacementException import InvalidPlacementException
from .Project import Project
import pygame as pg
from PIL import Image
import json
#should have two layers of images for grass and water and then separately for grass and such
class GameData:
    __slots__ = ["noBlockX","noBlockY","width","height","imgIndxMap","imgArr","groundData","rockTreeData","tileToColor","offsetArr","sizeArr","transpImgArr","redTintColor","transRedArr","projectNames","indxImgMap","game","disableMaintBar","maintOffsetArr"]
    def __init__(self,noBlockX,noBlockY,width,height,game,*args):
        self.width = width 
        self.height = height
        self.imgIndxMap = {}
        self.indxImgMap = {}
        self.tileToColor = {}
        self.imgArr = []
        self.transpImgArr = []
        self.transRedArr = []
        
        self.offsetArr = []
        self.maintOffsetArr = []

        self.sizeArr = []
        self.game = game
        self.redTintColor = (255,0,0)
        #self.loadImages()
        self.projectNames = {}
        self.loadImages()

        self.disableMaintBar = {"tree":0,"rock":0}

        if len(args) == 2 : 
            self.noBlockX = self.imgArr[self.imgIndxMap["mapWaterGrass"]].get_height()
            self.noBlockY = self.imgArr[self.imgIndxMap["mapWaterGrass"]].get_width()
            self.groundData = self.createGroundData()    
            self.rockTreeData = self.createRockTreeData()
        else: 
            self.noBlockX = noBlockX
            self.noBlockY = noBlockY
            self.groundData   = self.createGroundDataDebug()
            self.rockTreeData = self.createRockTreeDebug()
    #didnt create separate function to only generate grass
    def createGroundData(self):
        groundData = [[-1 for y in range(self.noBlockY)] for x in range(self.noBlockX)]
        
        for x in range(self.noBlockX):
            for y in range(self.noBlockY):
                #not precalculating positions for now
                #flipping as changed convention before and causing problems when reading image
                pixel = self.imgArr[self.imgIndxMap["mapWaterGrass"]].get_at((y,x))
                #print(pixel)
                if pixel == self.tileToColor["block"]:
                    curDict = {"tile":self.imgIndxMap["block"]}
                    groundData[x][y] = curDict
                elif pixel == self.tileToColor["water"]: 
                    curDict = {"tile":self.imgIndxMap["water"]}
                    groundData[x][y] = curDict
                else:
                    pass
                    #print(f"Unrecognized pixel at {x},{y} with colour {pixel}")
                # curDict = {"tile":self.imgIndxMap["block"]}
                # groundData[x][y] = curDict
        return groundData
    def checkGroundTiles(self,x,y,tileName):
        incorrectTile = "water"
        if tileName == "Dam":
            incorrectTile = "block"
        xSize,ySize = self.sizeArr[self.imgIndxMap[tileName]]
#        if (x < (xSize -1) or y+ySize > self.noBlockY or x+xSize > self.noBlockX or y < ySize-1):
#            return False
        if(y < (ySize - 1) or y > self.noBlockY or x +xSize > self.noBlockX or x < 0):
            return False
        for i in range(xSize):
            for j in range(ySize):
                if self.groundData[x+i][y-j]["tile"] == self.imgIndxMap[incorrectTile]:
                    return False
        return True
    def checkSpacePresent(self,x,y,tileName):
        xSize,ySize = self.sizeArr[self.imgIndxMap[tileName]]
#        if(x <(xSize-1) or y+ySize > self.noBlockY or x+xSize > self.noBlockX or y < ySize-1):
#            return False
        if(y < (ySize - 1) or y > self.noBlockY or x +xSize > self.noBlockX or x < 0):
            return False
        for i in range(xSize):
            for j in range(ySize):
                if self.rockTreeData[x+i][y-j] != None:
                    return False
        
        return True
    def checkPlacementValid(self,x,y,tileName):
        isSpacePresent = self.checkSpacePresent(x,y,tileName)
        isGroundTileCorr = self.checkGroundTiles(x,y,tileName)
        return isSpacePresent and isGroundTileCorr
    def blockNeighbourSlots(self,x,y,size,rockTreeData,tileName):
        xSize,ySize = size 
#        if(x < (xSize-1) or y+ySize > self.noBlockY):
#            raise InvalidPlacementException(f"The placement of object is invalid there is overlap between some two objects at {x},{y} {tileName}")
        if(y < (ySize - 1) or y > self.noBlockY or x +xSize > self.noBlockX or x < 0):
            return False
        for i in range(xSize):
            for j in range(ySize):
                if rockTreeData[x+i][y-j] == None:
                    rockTreeData[x+i][y-j] = (-i,j)
                else:
                    overLapObj = rockTreeData[x+i][y-j]
                    overlapCoord = (x+i,y-j)
                    tile = None
                    if type(overLapObj) == tuple:
                        overlapCoord = (overlapCoord[0]+overLapObj[0],overlapCoord[1]+overLapObj[1])
                        tile = rockTreeData[overlapCoord[0]][overlapCoord[1]]["tile"]
                    else:
                        tile = rockTreeData[overlapCoord[0]][overlapCoord[1]]["tile"]
                    raise InvalidPlacementException(f"The placement of object is invalid there is overlap between some two objects located at:{x},{y} {tileName} and {overlapCoord[0]},{overlapCoord[1]} {self.indxImgMap[tile]}")
        rockTreeData[x][y] = self.createProject(tileName,(x,y))
    def placeObject(self,x,y,tileName):
        curSize = self.sizeArr[self.imgIndxMap[tileName]]
        self.blockNeighbourSlots(x,y,curSize,self.rockTreeData,tileName)
        return True
    def createRockTreeData(self):
        rockTreeData = [[None for y in range(self.noBlockY)] for x in range(self.noBlockX)]
        for x in range(self.noBlockX):
            for y in range(self.noBlockY):
                #not precalculating positions for now
                pixel = self.imgArr[self.imgIndxMap["mapTreeRock"]].get_at((y,x))
                for key in self.projectNames:
                    if pixel == self.tileToColor[key]:
                        curSize = self.sizeArr[self.imgIndxMap[key]]
                        self.blockNeighbourSlots(x,y,curSize,rockTreeData,key)
                        self.game.powerManagement.handleProj(key)
                        self.game.waterManagement.handleProj(key)
        return rockTreeData
    def createGroundDataDebug(self):
        groundData = [[-1 for y in range(self.noBlockY)] for x in range(self.noBlockX)]
        for x in range(self.noBlockX):
            for y in range(self.noBlockY):
                curDict = {"tile":self.imgIndxMap["block"]}
        return groundData
    def createRockTreeDebug(self):
        rockTreeData = [[None for y in range(self.noBlockY)] for x in range(self.noBlockX)]
        return rockTreeData
    #temporarily removing reload offsets
    def reloadOffsets(self):
        pass
    def loadImages(self):
        f = open("res/json/imageMetaDataAlt.json")
        data = json.load(f)
        mapData = data["mapRelated"]
        groundData = data["groundRelated"]
        projData = data["projRelated"]

        self.loadMapImages(mapData)
        self.loadBlockImages(groundData)
        self.loadProjectImages(projData)
    def loadBlockImages(self,blockData):
        for key in blockData:
            curImg = ldImage(blockData[key]["path"]["normal"])
            curTransparent = None
            curTransRed = None
            
            self.imgIndxMap[key] = len(self.imgArr)
            self.indxImgMap[len(self.imgArr)] = key

            self.imgArr.append(curImg)
            self.transpImgArr.append(curTransparent)
            self.transRedArr.append(curTransRed)

            curOffset = (0,0)
            self.offsetArr.append(curOffset)

            self.maintOffsetArr.append(None)

            curSize = (1,1)
            self.sizeArr.append(curSize)
            self.tileToColor[key] = parseColour(blockData[key]["colour"])
    def loadMapImages(self,mapData):
        for key in mapData:
            curImg = ldImage(mapData[key]["path"]["normal"])
            curTransparent = None
            curTransRed = None
            
            self.imgIndxMap[key] = len(self.imgArr)
            self.indxImgMap[len(self.imgArr)] = key

            self.imgArr.append(curImg)
            self.transpImgArr.append(curTransparent)
            self.transRedArr.append(curTransRed)

            curOffset = (0,0)
            self.offsetArr.append(curOffset)

            self.maintOffsetArr.append(None)

            curSize = (1,1)
            self.sizeArr.append(curSize)
    def loadProjectImages(self,projData):
        for key in projData:
            self.projectNames[key] = 0
            curImg = ldImage(projData[key]["path"]["normal"])
            curTransparent = None
            curTransparent = ldImage(projData[key]["path"]["transparent"])

            self.imgIndxMap[key] = len(self.imgArr)
            self.indxImgMap[len(self.imgArr)] = key

            curTransRed = curTransparent.__copy__()
            curTransRed.fill((255,0,0),special_flags=pg.BLEND_ADD)

            self.transRedArr.append(curTransRed)
            self.imgArr.append(curImg)
            self.transpImgArr.append(curTransparent)

            #check if can remove curCoord and offset as needed
            curCoord = parseTuple(projData[key]["offset"])
            self.offsetArr.append(curCoord)

            self.maintOffsetArr.append(projData[key]["maintOffset"])

            curSize = parseTuple(projData[key]["size"])
            self.sizeArr.append(curSize)
            self.tileToColor[key] = parseColour(projData[key]["colour"])
    def writeRockTreeData(self,imagePath):
        image = Image.new('RGB',(self.noBlockY,self.noBlockX))
        for x in range(self.noBlockX):
            for y in range(self.noBlockY):
                curDict = self.rockTreeData[x][y]
                if type(curDict) == dict:
                    imgIndx = curDict["tile"]
                    imgName = self.indxImgMap[imgIndx]
                    curColor = self.tileToColor[imgName]
                    image.putpixel((y,x),curColor)
        image.save(imagePath)
#    def createProject(self,projName,pos,mode="normal"):
#        return {"tile":self.imgIndxMap[projName],"pos":pos,"mode":mode}
    def createProject(self,projName,pos,mode="normal"):
        projIndx = self.imgIndxMap[projName]
        if projName in self.disableMaintBar:
            return Project(projIndx,pos,self.maintOffsetArr[projIndx],self.game.manager,mode,False)
        else:
            return Project(projIndx,pos,self.maintOffsetArr[projIndx],self.game.manager,mode)
    def updateProjMaintBar(self,totalOffset):
        for x in range(self.noBlockX):
            for y in range(self.noBlockY):
                if type(self.rockTreeData[x][y]) == Project:
                    self.rockTreeData[x][y].updateMaintBar(totalOffset)
        