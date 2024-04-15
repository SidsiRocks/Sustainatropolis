from typing import Any
import json

class WaterManagemetSystem :

    def __init__ (self) :
        findDict = json.load(open("game/waterManagement.json"))
        self.prodUncleanWater = findDict["produceUncleanWater"] 
        self.consUncleanWaterDic = findDict["consumeUncleanWater"]

        self.prodCleanWater = findDict["produceCleanWater"]
        self.consCleanWaterDic = findDict["consumeCleanWater"]

        self.prodStoreWater = findDict["produceStoreWater"]
        self.consStoreWaterDic = findDict["consumeStoreWater"]

        self.prodSewage = findDict["produceSewage"]
        self.consSewageDic = findDict["sewagePlant"]

        self.unCleanWater = 0
        self.consUnCleanWater = 0

        self.cleanWater = 0
        self.consCleanWater = 0

        self.storeWater = 0
        self.consStoreWater = 0

        self.sewageWater = 0
        self.consSewageWater = 0

    def handleProj(self,projName):
        unCleanWaterTpl,cleanWaterTpl,storeWaterTpl,sewageWaterTpl = self.updateVal(projName)
        
        self.unCleanWater,self.consUnCleanWater = unCleanWaterTpl
        self.cleanWater,self.consCleanWater = cleanWaterTpl
        self.storeWater,self.consStoreWater = storeWaterTpl
        self.sewageWater,self.consSewageWater = sewageWaterTpl

    def updateVal(self,projName):
        if projName in self.prodUncleanWater:
            unCleanWater = self.unCleanWater + self.prodUncleanWater[projName]
        if projName in self.consUncleanWaterDic:
            consUnCleanWater = self.consUnCleanWater + self.consUncleanWaterDic[projName]

        if projName in self.prodCleanWater:
            cleanWater = self.cleanWater + self.prodCleanWater[projName]
        if projName in self.consCleanWaterDic:
            consCleanWater = self.consCleanWater + self.consCleanWaterDic[projName]

        if projName in self.prodStoreWater:
            storeWater = self.storeWater + self.prodStoreWater[projName]
        if projName in self.consStoreWaterDic:
            consStoreWater = self.consStoreWater + self.consStoreWaterDic[projName]     
    
        if projName in self.prodSewage:
            sewageWater = self.sewageWater + self.prodSewage[projName]
        if projName in self.consSewageDic:
            consSewageWater = self.consSewageWater + self.consSewageDic[projName]        

        unCleanWaterTpl = (unCleanWater,consUnCleanWater)
        cleanWaterTpl = (cleanWater,consCleanWater)
        storeWaterTpl = (storeWater,consStoreWater)
        sewageWaterTpl = (sewageWater,consSewageWater)

        return (unCleanWaterTpl,cleanWaterTpl,storeWaterTpl,sewageWaterTpl)

    def waterDataTplValid(self,tpl):
        unCleanWaterTpl,cleanWaterTpl,storeWaterTpl,sewageWaterTpl = tpl
        isValid1 = (unCleanWaterTpl[0] >= unCleanWaterTpl[1]) and (cleanWaterTpl[0] >= cleanWaterTpl[1])
        isValid2 = (storeWaterTpl[0] >= storeWaterTpl[1]) and (sewageWaterTpl[0] >= sewageWaterTpl[1])
        return isValid1 and isValid2
    
    def validProjPlace(self,projName):
        return self.waterDataTplValid(self.updateVal(projName))
