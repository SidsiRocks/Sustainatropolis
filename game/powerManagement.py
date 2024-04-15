import json
class PowerManagement:
    def __init__(self):
        findDict = json.load("game/powerManagement.json")
        self.powerProduceDic = findDict["producers"]
        self.powerConsumeDic = findDict["consumers"]

        self.powerPlants = list(self.powerProd.keys())
        self.powerCons = list(self.powerCons.keys())


        self.noPowerPlantDict = self.createPlantDict(self.powerPlants)
        self.noPowerReqDict = self.createPowerDict(self.powerReq)
        self.curPowerProd = 0
        self.curPowerCons = 0


    def createPlantDict(self,powerPlant):
        resultDict = {}
        for plant,powerProd in powerPlant:
            resultDict[plant] = 0
        return resultDict
    def createPowerDict(self,powerReq):
        resultDict = {}
        for req,powerUsed in powerReq:
            resultDict[req] = 0
        return resultDict

    def handleProj(self,projName):
        if projName in self.noPowerPlantDict:
            self.noPowerPlantDict[projName] = self.noPowerPlantDict[projName] + 1
            self.curPowerProd += self.powerProduceDic[projName]
        elif projName in self.noPowerReqDict:
            self.noPowerReqDict[projName] = self.noPowerReqDict[projName] + 1
            self.curPowerCons += self.powerConsumeDic[projName]
    
    def getPowerProd(self):
        return self.curPowerProd
    def getPowerCons(self):
        return self.curPowerCons
