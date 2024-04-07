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
            self.noBlockX = ldImage(args[0]).get_width()
            self.noBlockY = ldImage(args[0]).get_height()
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
                pixel = self.imgArr[self.imgIndxMap["mapWaterGrass"]].get_at((x,y))
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
                pixel = self.imgArr[self.imgIndxMap["mapTreeRock"]].get_at((x,y))
                #print(pixel)
                if pixel == (93,61,0,255):
                    curDict = {"tile":self.imgIndxMap["rock"]}
                    rockTreeData[x][y] = curDict
                elif pixel == (0,93,6,255) : 
                    curDict = {"tile":self.imgIndxMap["tree"]}
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