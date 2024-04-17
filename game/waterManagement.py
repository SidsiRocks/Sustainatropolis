from typing import Any
import json
from .statisticsUI import StatisticsWindow

class WaterManagement:

    def __init__ (self,game) :
        findDict = json.load(open("res/json/waterManagement.json"))
        self.JSONdict = findDict
        self.prodUncleanWater = findDict["produceUncleanWater"] 
        self.consUncleanWaterDic = findDict["consumeUncleanWater"]

        self.prodCleanWater = findDict["produceCleanWater"]
        self.consCleanWaterDic = findDict["consumeCleanWater"]

        self.prodStoreWater = findDict["produceStoreWater"]
        self.consStoreWaterDic = findDict["consumeStoreWater"]

        self.prodSewage = findDict["produceSewage"]
        self.consSewageDic = findDict["consumeSewage"]

        self.unCleanWater = 0
        self.consUnCleanWater = 0

        self.cleanWater = 0
        self.consCleanWater = 0

        self.storeWater = 0
        self.consStoreWater = 0

        self.sewageWater = 0
        self.consSewageWater = 0
        self.countProjects = findDict["countProjects"]
        self.offSets = findDict["offsets"]
        
        self.game = game

    def waterDataTplValid(self,tpl):
        pass
    
    def validProjPlace(self,projName):
        pass
    def setStats(self,statWin:StatisticsWindow):
        statWin.setStats("Unclean Water",self.consUnCleanWater,self.unCleanWater)
        statWin.setStats("Clean Water",self.consCleanWater,self.cleanWater)
        statWin.setStats("Store Water",self.consStoreWater,self.storeWater)
        statWin.setStats("Sewage Water",self.consSewageWater,self.sewageWater)

    def handleProj(self,project) :
    
        if project in self.countProjects :
            self.countProjects[project] += 1
        else : 
            self.countProjects[project] = 1
        
        self.updateVals()
    def updateVals(self) :
        self.unCleanWater = 0 
        self.consUnCleanWater = 0
        self.cleanWater = 0 
        self.consCleanWater = 0
        self.storeWater = 0
        self.consStoreWater = 0
        self.sewageWater = 0
        self.consSewageWater = 0

        for proj in self.countProjects :

            if proj in self.JSONdict["produceUncleanWater"] :
                self.unCleanWater += (self.JSONdict["produceUncleanWater"][proj] + self.offSets[proj] )* self.countProjects[proj] 
            
            if proj in self.JSONdict["consumeUncleanWater"] :
                self.consUnCleanWater += (self.JSONdict["consumeUncleanWater"][proj] + self.offSets[proj] ) * self.countProjects[proj]
            
            if proj in self.JSONdict["produceCleanWater"] :
                self.cleanWater += (self.JSONdict["produceCleanWater"][proj] + self.offSets[proj] ) * self.countProjects[proj]
            
            if proj in self.JSONdict["consumeCleanWater"] :
                self.consCleanWater += (self.JSONdict["consumeCleanWater"][proj] + self.offSets[proj] ) * self.countProjects[proj]
            
            if proj in self.JSONdict["produceStoreWater"] :
                self.storeWater += (self.JSONdict["produceStoreWater"][proj] + self.offSets[proj] ) * self.countProjects[proj]
            
            if proj in self.JSONdict["consumeStoreWater"] :
                self.consStoreWater += (self.JSONdict["consumeStoreWater"][proj] + self.offSets[proj] ) * self.countProjects[proj]
            
            if proj in self.JSONdict["produceSewage"] :
                self.sewageWater += (self.JSONdict["produceSewage"][proj] + self.offSets[proj] ) * self.countProjects[proj]
            
            if proj in self.JSONdict["consumeSewage"] :
                self.consSewageWater += (self.JSONdict["consumeSewage"][proj] + self.offSets[proj] ) * self.countProjects[proj]

        self.consUnCleanWater = min(self.consUnCleanWater,self.unCleanWater)
        self.cleanWater = min(self.cleanWater,self.consUnCleanWater)
        self.consCleanWater = min(self.consCleanWater,self.cleanWater)
        self.storeWater = min(self.storeWater,self.consCleanWater)
        self.consStoreWater = min(self.consStoreWater,self.storeWater)
        self.setStats(self.game.mainGameUI.statsWindowWrapper)
    def processNotifs(self,notif) :
        if notif == "Reset" :
            for proj,changes in self.offSets.items() : 
                self.offSets[proj] = 0  
                return 
        for update in self.JSONdict["offsetsFromRegular"][notif] :
            self.offSets[update] = self.JSONdict["offsetsFromRegular"][notif][update]

