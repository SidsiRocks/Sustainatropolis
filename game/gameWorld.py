from .util import ldImage,parseColour,parseTuple
from .InvalidPlacementException import InvalidPlacementException
import json
#should have two layers of images for grass and water and then separately for grass and such
class GameData:
    __slots__ = ["noBlockX","noBlockY","width","height","imgIndxMap","imgArr","groundData","rockTreeData","tileToColor","offsetArr","sizeArr"]
    def __init__(self,noBlockX,noBlockY,width,height,*args):
        self.width = width 
        self.height = height
        self.imgIndxMap = {}
        self.tileToColor = {}
        self.imgArr = []
        self.offsetArr = []
        self.sizeArr = []
        #self.loadImages()
        self.loadImagesFromJSON()
        if len(args) == 2 : 
            self.noBlockX = ldImage(args[0]).get_height()
            self.noBlockY = ldImage(args[0]).get_width()
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

                # curDict = {"tile":self.imgIndxMap["block"]}
                # groundData[x][y] = curDict
        return groundData
    def blockNeighbourSlots(self,x,y,size,rockTreeData,tileName):
        xSize,ySize = size 
        if(x < (xSize-1) or y+ySize > self.noBlockY):
            raise InvalidPlacementException(f"The placement of object is invalid there is overlap between some two objects at {x},{y} {tileName}")
        for i in range(xSize):
            for j in range(ySize):
                if rockTreeData[x-i][y+j] == None:
                    rockTreeData[x-i][y+j] = (i,-j)
                else:
                    raise InvalidPlacementException(f"The placement of object is invalid there is overlap between some two objects {x},{y} {tileName}")
        rockTreeData[x][y] = {"tile":self.imgIndxMap[tileName]}
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
                #print(pixel)
                if pixel == self.tileToColor["rock"]:
                    curSize = self.sizeArr[self.imgIndxMap["rock"]]
                    self.blockNeighbourSlots(x,y,curSize,rockTreeData,"rock")
                elif pixel == self.tileToColor["tree"]: 
                    curSize = self.sizeArr[self.imgIndxMap["tree"]]
                    self.blockNeighbourSlots(x,y,curSize,rockTreeData,"tree")
                elif pixel == self.tileToColor["waterTreatment"]:
                    curSize = self.sizeArr[self.imgIndxMap["waterTreatment"]]
                    self.blockNeighbourSlots(x,y,curSize,rockTreeData,"waterTreatment")
                elif pixel == self.tileToColor["sewagePlant"]:
                    curSize = self.sizeArr[self.imgIndxMap["sewagePlant"]]
                    self.blockNeighbourSlots(x,y,curSize,rockTreeData,"sewagePlant")
                elif pixel == self.tileToColor["waterPump"]:
                    curSize = self.sizeArr[self.imgIndxMap["waterPump"]]
                    self.blockNeighbourSlots(x,y,curSize,rockTreeData,"waterPump")
                elif pixel == self.tileToColor["purificationPlant"]:
                    curSize = self.sizeArr[self.imgIndxMap["purificationPlant"]]
                    self.blockNeighbourSlots(x,y,curSize,rockTreeData,"purificationPlant")
                elif pixel == self.tileToColor["industrialPlant"]:
                    curSize = self.sizeArr[self.imgIndxMap["industrialPlant"]]
                    self.blockNeighbourSlots(x,y,curSize,rockTreeData,"industrialPlant")
                elif pixel == self.tileToColor["solarPowerPlant"]:
                    curSize = self.sizeArr[self.imgIndxMap["solarPowerPlant"]]
                    self.blockNeighbourSlots(x,y,curSize,rockTreeData,"solarPowerPlant")
                elif pixel == self.tileToColor["powerPlant"]:
                    curSize = self.sizeArr[self.imgIndxMap["powerPlant"]]
                    self.blockNeighbourSlots(x,y,curSize,rockTreeData,"powerPlant")
                elif pixel == self.tileToColor["windMill"]:
                    curSize = self.sizeArr[self.imgIndxMap["windMill"]]
                    self.blockNeighbourSlots(x,y,curSize,rockTreeData,"windMill")
                else:
                    #ignoring if someother coulour so include water and grass for refrence in the image
                    pass
                # curDict = {"tile":self.imgIndxMap["block"]}
                # groundData[x][y] = curDict
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
    def reloadOffsets(self):
        f = open("game/imageMetaData.json")
        data = json.load(f)
        for key in data:
            curIndx = self.imgIndxMap[key]
            curCoord = parseTuple(data[key]["offset"])
            self.offsetArr[curIndx] = curCoord
    def loadImagesFromJSON(self):
        f = open("game/imageMetaData.json")
        data = json.load(f)
        for key in data:
            curImg = ldImage(data[key]["path"])
            self.imgIndxMap[key] = len(self.imgArr)
            self.imgArr.append(curImg)
            curCoord = parseTuple(data[key]["offset"])
            self.offsetArr.append(curCoord)
            curSize = parseTuple(data[key]["size"])
            self.sizeArr.append(curSize)
            if "colour" in data[key]:
                self.tileToColor[key] = parseColour(data[key]["colour"])