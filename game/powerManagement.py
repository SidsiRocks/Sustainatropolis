import json
from .statisticsUI import StatisticsWindow
class PowerManagement:
    def __init__(self,game):
        findDict = json.load(open("res/json/powerManagement.json"))
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
        self.game = game

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

        self.setStats(self.game.mainGameUI.statsWindowWrapper)

    def setStats(self,statWin:StatisticsWindow):
        statWin.setStats("Power Usage",self.curPowerCons,self.curPowerProd)

    def validProjPlace(self,projName):
        print(f"self.powerConsumeDic:{self.powerConsumeDic}")
        if projName in self.powerConsumeDic:
            if (self.curPowerCons + self.powerConsumeDic[projName]) <= self.curPowerProd:
                return True
            else:
                return False
        return True

    def getPowerReqForProj(self,projName):
        if projName in self.powerConsumeDic:
            return self.powerConsumeDic[projName]
        
    def getPowerProd(self):
        return self.curPowerProd
    def getPowerCons(self):
        return self.curPowerCons
