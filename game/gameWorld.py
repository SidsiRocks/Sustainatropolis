from .util import ldImage
class GameData:
    __slots__ = ["noBlockX","noBlockY","width","height","imgIndxMap","imgArr","groundData"]
    def __init__(self,noBlockX,noBlockY,width,height,*args):
        if len(args) == 1 : 
            self.noBlockX = ldImage(args[0]).get_width()
            self.noBlockY = ldImage(args[0]).get_height()
        else : 
            self.noBlockX = noBlockX
            self.noBlockY = noBlockY
        self.width = width 
        self.height = height
        self.imgIndxMap = {}
        self.imgArr = []
        self.loadImages()
        self.groundData = self.createGroundData()    
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
                elif pixel == (192,192,192,255) :
                    curDict = {"tile":self.imgIndxMap["rock"]}
                    groundData[x][y] = curDict
                else : 
                    curDict = {"tile":self.imgIndxMap["tree"]}
                    groundData[x][y] = curDict

                # curDict = {"tile":self.imgIndxMap["block"]}
                # groundData[x][y] = curDict
        return groundData
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