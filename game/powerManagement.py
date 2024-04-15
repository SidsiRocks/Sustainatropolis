import json
class PowerManagement:
    def __init__(self):
        findDict = json.load(open("game/powerManagement.json"))
        self.powerProduceDic = findDict["producers"]
        self.powerConsumeDic = findDict["consumers"]

        self.powerPlants = list(self.powerProduceDic.keys())
        self.powerCons = list(self.powerConsumeDic.keys())


        self.noPowerPlantDict = self.createPlantDict(self.powerPlants)
        self.noPowerReqDict = self.createPowerDict(self.powerCons)
        print(f"self.noPowerPlantDict is:{self.noPowerPlantDict}")
        print(f"self.noPowerReqDict is:{self.noPowerReqDict}")
        
        self.curPowerProd = 0
        self.curPowerCons = 0


    def createPlantDict(self,powerPlant):
        resultDict = {}
        for plant in powerPlant:
            resultDict[plant] = 0
        return resultDict
    def createPowerDict(self,powerReq):
        resultDict = {}
        for req in powerReq:
            resultDict[req] = 0
        return resultDict

    def handleProj(self,projName):
        if projName in self.noPowerPlantDict:
            self.noPowerPlantDict[projName] = self.noPowerPlantDict[projName] + 1
            self.curPowerProd += self.powerProduceDic[projName]
        elif projName in self.noPowerReqDict:
            self.noPowerReqDict[projName] = self.noPowerReqDict[projName] + 1
            self.curPowerCons += self.powerConsumeDic[projName]
    
    def validProjPlace(self,projName):
        if projName in self.noPowerReqDict:
            if (self.curPowerCons + self.powerConsumeDic[projName]) <= self.curPowerProd:
                return False
        return True
    def getPowerProd(self):
        return self.curPowerProd
    def getPowerCons(self):
        return self.curPowerCons
