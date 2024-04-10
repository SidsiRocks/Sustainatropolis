from .util import ldImage
#should have two layers of images for grass and water and then separately for grass and such
class GameData:
    __slots__ = ["noBlockX","noBlockY","width","height","imgIndxMap","imgArr","groundData","rockTreeData"]
    def __init__(self,noBlockX,noBlockY,width,height,*args):
        self.width = width 
        self.height = height
        self.imgIndxMap = {}
        self.imgArr = []
        self.loadImages()
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
                if pixel == (0,255,0,255):
                    curDict = {"tile":self.imgIndxMap["block"]}
                    groundData[x][y] = curDict
                elif pixel == (0,255,255,255) : 
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
                if pixel == (93,61,0,255):
                    curDict = {"tile":self.imgIndxMap["rock"]}
                    rockTreeData[x][y] = curDict
                elif pixel == (0,93,6,255) : 
                    curDict = {"tile":self.imgIndxMap["tree"]}
                    rockTreeData[x][y] = curDict
                elif pixel == (23,20,157):
                    curDict = {"tile":self.imgIndxMap["waterTreatment"]}
                    rockTreeData[x][y] = curDict
                elif pixel == (23,207,40):
                    curDict = {"tile":self.imgIndxMap["sewagePlant"]}
                    rockTreeData[x][y] = curDict
                elif pixel == (158,37,21):
                    curDict = {"tile":self.imgIndxMap["waterPump"]}
                    rockTreeData[x][y] = curDict
                elif pixel == (169,16,152):
                    curDict = {"tile":self.imgIndxMap["purificationPlant"]}
                    rockTreeData[x][y] = curDict
                elif pixel == (56,57,56):
                    curDict = {"tile":self.imgIndxMap["industrialPlant"]}
                    rockTreeData[x][y] = curDict
                elif pixel == (251,254,105):
                    curDict = {"tile":self.imgIndxMap["solarPowerPlant"]}
                    rockTreeData[x][y] = curDict                    
                elif pixel == (55,209,226):
                    curDict = {"tile":self.imgIndxMap["powerPlant"]}
                    rockTreeData[x][y] = curDict                    
                elif pixel == (243,243,243):
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
    def loadImages(self):
        blockImg = ldImage("res/graphics/block.png")
        self.imgIndxMap["block"] = 0
        self.imgArr.append(blockImg)
        
        rockImg  = ldImage("res/graphics/rock.png")
        self.imgIndxMap["rock"] = 1
        self.imgArr.append(rockImg)

        treeImg  = ldImage("res/graphics/tree.png")
        self.imgIndxMap["tree"] = 2
        self.imgArr.append(treeImg)

        mapWaterGrassImg = ldImage("res/graphics/mapWaterGrass.png")
        self.imgIndxMap["mapWaterGrass"] = 3
        self.imgArr.append(mapWaterGrassImg)

        waterImg = ldImage("res/graphics/waterfallEndE.png")
        self.imgIndxMap["water"] = 4
        self.imgArr.append(waterImg)

        treeImg = ldImage("res/graphics/tree.png")
        self.imgIndxMap["tree"] = 5
        self.imgArr.append(treeImg)

        mapTreeRockImg = ldImage("res/graphics/mapTreeRock.png")
        self.imgIndxMap["mapTreeRock"] = 6
        self.imgArr.append(mapTreeRockImg)

        buildingOneImg = ldImage("res/graphics/building01.png")
        self.imgIndxMap["building01"] = 7
        self.imgArr.append(buildingOneImg)

        buildingTwoImg = ldImage("res/graphics/building01.png")
        self.imgIndxMap["building02"] = 8
        self.imgArr.append(buildingTwoImg)

        waterPlantImg = ldImage("res/graphics/waterTreatment3by3preserveAspect.png")
        self.imgIndxMap["waterTreatment"] = 9
        self.imgArr.append(waterPlantImg)
        #23 20 157

        sewagePlantImg = ldImage("res/graphics/sewageTreatmentPlantResize.png")
        self.imgIndxMap["sewagePlant"] = 10
        self.imgArr.append(sewagePlantImg)
        #23 207 40

        waterPumpImg = ldImage("res/graphics/pumpingPlantResize.png")
        self.imgIndxMap["waterPump"] = 11
        self.imgArr.append(waterPumpImg)
        #158 37 21


        purificationPlant = ldImage("res/graphics/PurificationPlantResize.png")
        self.imgIndxMap["purificationPlant"] = 12
        self.imgArr.append(purificationPlant)
        #169 16 152

        #may want to resize the pumping station

        industrialPlant = ldImage("res/graphics/IndustrialPlantResize.png")
        self.imgIndxMap["industrialPlant"] = 13
        self.imgArr.append(industrialPlant)
        #56 57 56

        solarPowerPlant = ldImage("res/graphics/SolarPowerPlantResize.png")
        self.imgIndxMap["solarPowerPlant"] = 14
        self.imgArr.append(solarPowerPlant)
        #251 254 105

        powerPlant = ldImage("res/graphics/powerPlantResize.png")
        self.imgIndxMap["powerPlant"] = 15
        self.imgArr.append(powerPlant)
        #55 209 226

        windMill = ldImage("res/graphics/windMillIndivResize.png")
        self.imgIndxMap["windMill"] = 16
        self.imgArr.append(windMill)
        #243 243 243