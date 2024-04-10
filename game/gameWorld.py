from .util import ldImage,parseColour
import json
#should have two layers of images for grass and water and then separately for grass and such
class GameData:
    __slots__ = ["noBlockX","noBlockY","width","height","imgIndxMap","imgArr","groundData","rockTreeData","tileToColor"]
    def __init__(self,noBlockX,noBlockY,width,height,*args):
        self.width = width 
        self.height = height
        self.imgIndxMap = {}
        self.tileToColor = {}
        self.imgArr = []
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
    def loadImagesFromJSON(self):
        f = open("game/imageMetaData.json")
        data = json.load(f)
        for key in data:
            curImg = ldImage(data[key]["path"])
            self.imgIndxMap[key] = len(self.imgArr)
            self.imgArr.append(curImg)
            if "colour" in data[key]:
                self.tileToColor[key] = parseColour(data[key]["colour"])
    def loadImages(self):
        blockImg = ldImage("res/graphics/block.png")
        self.imgIndxMap["block"] = len(self.imgArr)
        self.imgArr.append(blockImg)
        self.tileToColor["block"] = (0,255,0,255)
        
        rockImg  = ldImage("res/graphics/rock.png")
        self.imgIndxMap["rock"] = len(self.imgArr)
        self.imgArr.append(rockImg)
        self.tileToColor["rock"] = (93,61,0,255)
        #93 61 0

        treeImg  = ldImage("res/graphics/tree.png")
        self.imgIndxMap["tree"] = len(self.imgArr)
        self.imgArr.append(treeImg)
        self.tileToColor["tree"] = (0,93,6,255)
        #0 93 6

        mapWaterGrassImg = ldImage("res/graphics/mapWaterGrass.png")
        self.imgIndxMap["mapWaterGrass"] = len(self.imgArr)
        self.imgArr.append(mapWaterGrassImg)

        waterImg = ldImage("res/graphics/waterfallEndE.png")
        self.imgIndxMap["water"] = len(self.imgArr)
        self.imgArr.append(waterImg)
        self.tileToColor["water"] = (0,255,255,255)

        mapTreeRockImg = ldImage("res/graphics/mapTreeRock.png")
        self.imgIndxMap["mapTreeRock"] = len(self.imgArr)
        self.imgArr.append(mapTreeRockImg)

        buildingOneImg = ldImage("res/graphics/building01.png")
        self.imgIndxMap["building01"] = len(self.imgArr)
        self.imgArr.append(buildingOneImg)

        buildingTwoImg = ldImage("res/graphics/building02.png")
        self.imgIndxMap["building02"] = len(self.imgArr)
        self.imgArr.append(buildingTwoImg)

        waterPlantImg = ldImage("res/graphics/waterTreatment3by3preserveAspect.png")
        self.imgIndxMap["waterTreatment"] = len(self.imgArr)
        self.imgArr.append(waterPlantImg)
        self.tileToColor["waterTreatment"] = (23,20,157)
        #23 20 157

        sewagePlantImg = ldImage("res/graphics/sewageTreatmentPlantResize.png")
        self.imgIndxMap["sewagePlant"] = len(self.imgArr)
        self.imgArr.append(sewagePlantImg)
        self.tileToColor["sewagePlant"] = (23,207,40)
        #23 207 40

        waterPumpImg = ldImage("res/graphics/pumpingPlantResize.png")
        self.imgIndxMap["waterPump"] = len(self.imgArr)
        self.imgArr.append(waterPumpImg)
        self.tileToColor["waterPump"] = (158,37,21)
        #158 37 21


        purificationPlant = ldImage("res/graphics/PurificationPlantResize.png")
        self.imgIndxMap["purificationPlant"] = len(self.imgArr)
        self.imgArr.append(purificationPlant)
        self.tileToColor["purificationPlant"] = (169,16,152)
        #169 16 152

        #may want to resize the pumping station

        industrialPlant = ldImage("res/graphics/IndustrialPlantResize.png")
        self.imgIndxMap["industrialPlant"] = len(self.imgArr)
        self.imgArr.append(industrialPlant)
        self.tileToColor["industrialPlant"] = (56,57,56)
        #56 57 56

        solarPowerPlant = ldImage("res/graphics/SolarPowerPlantResize.png")
        self.imgIndxMap["solarPowerPlant"] = len(self.imgArr)
        self.imgArr.append(solarPowerPlant)
        self.tileToColor["solarPowerPlant"] = (251,254,105)
        #251 254 105

        powerPlant = ldImage("res/graphics/powerPlantResize.png")
        self.imgIndxMap["powerPlant"] = len(self.imgArr)
        self.imgArr.append(powerPlant)
        self.tileToColor["powerPlant"] = (55,209,226)
        #55 209 226

        windMill = ldImage("res/graphics/windMillIndivResize.png")
        self.imgIndxMap["windMill"] = len(self.imgArr)
        self.imgArr.append(windMill)
        self.tileToColor["windMill"] = (243,243,243)
        #243 243 243