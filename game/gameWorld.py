from .util import ldImage,parseColour,parseTuple
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
    def createRockTreeData(self):
        rockTreeData = [[None for y in range(self.noBlockY)] for x in range(self.noBlockX)]
        for x in range(self.noBlockX):
            for y in range(self.noBlockY):
                #not precalculating positions for now
                pixel = self.imgArr[self.imgIndxMap["mapTreeRock"]].get_at((y,x))
                #print(pixel)
                if pixel == self.tileToColor["rock"]:
                    curDict = {"tile":self.imgIndxMap["rock"]}
                    rockTreeData[x][y] = curDict
                elif pixel == self.tileToColor["tree"]: 
                    curDict = {"tile":self.imgIndxMap["tree"]}
                    rockTreeData[x][y] = curDict
                elif pixel == self.tileToColor["waterTreatment"]:
                    curDict = {"tile":self.imgIndxMap["waterTreatment"]}
                    rockTreeData[x][y] = curDict
                elif pixel == self.tileToColor["sewagePlant"]:
                    curDict = {"tile":self.imgIndxMap["sewagePlant"]}
                    rockTreeData[x][y] = curDict
                elif pixel == self.tileToColor["waterPump"]:
                    curDict = {"tile":self.imgIndxMap["waterPump"]}
                    rockTreeData[x][y] = curDict
                elif pixel == self.tileToColor["purificationPlant"]:
                    curDict = {"tile":self.imgIndxMap["purificationPlant"]}
                    rockTreeData[x][y] = curDict
                elif pixel == self.tileToColor["industrialPlant"]:
                    curDict = {"tile":self.imgIndxMap["industrialPlant"]}
                    rockTreeData[x][y] = curDict
                elif pixel == self.tileToColor["solarPowerPlant"]:
                    curDict = {"tile":self.imgIndxMap["solarPowerPlant"]}
                    rockTreeData[x][y] = curDict                    
                elif pixel == self.tileToColor["powerPlant"]:
                    curDict = {"tile":self.imgIndxMap["powerPlant"]}
                    rockTreeData[x][y] = curDict                    
                elif pixel == self.tileToColor["windMill"]:
                    curDict = {"tile":self.imgIndxMap["windMill"]}
                    rockTreeData[x][y] = curDict
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