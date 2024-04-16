from typing import Any
import json
from .statisticsUI import StatisticsWindow

class WaterManagement:

    def __init__ (self) :
        # self.statsManager = StatisticsWindow()
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
        self.countProjects = {
            "Dam" : 0 ,
            "purificationPlant" : 0 ,
            "waterPump" : 0 , 
            "sewagePlant" : 0 ,
            "waterTreatment" : 0 ,
            "WaterTank" : 0 ,
            "CityBuilding1" : 0 ,
            "CityBuilding2" : 0 ,
        }
        self.offSets = {
            "Dam" : 0 ,
            "purificationPlant" : 0 ,
            "waterPump" : 0 , 
            "sewagePlant" : 0 ,
            "waterTreatment" : 0 ,
            "WaterTank" : 0 ,
            "CityBuilding1" : 0 ,
            "CityBuilding2" : 0 ,
        }

    def waterDataTplValid(self,tpl):
        pass
    
    def validProjPlace(self,projName):
        pass
    def setStats(self,statWin:StatisticsWindow):
        statWin.setStats("unclean water",self.consUnCleanWater,self.unCleanWater)
        statWin.setStats("clean water",self.consCleanWater,self.cleanWater)
        statWin.setStats("store water",self.consStoreWater,self.storeWater)
        statWin.setStats("sewage water",self.consSewageWater,self.sewageWater)

    def projectPlanted(self,project) :
    
        if project in self.countProjects :
            print("incrementinf 1")
            self.countProjects[project] += 1
        else : 
            print("creating")
            self.countProjects[project] = 1
        print("Current ddictionary of proj freq")
        print(self.countProjects)

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
                # print('"projects with unclean water')
                # print(self.offSets[proj] , proj)
                # print(self.JSONdict["produceUncleanWater"][proj])
                # print(self.countProjects[proj])
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

        # self.statsManager.setStats("unclean water",self.unCleanWater,self.unCleanWater)
        # self.setStats()
        self.consUnCleanWater = min(self.consUnCleanWater,self.unCleanWater)
        self.cleanWater = min(self.cleanWater,self.consUnCleanWater)
        self.consCleanWater = min(self.consCleanWater,self.cleanWater)
        self.storeWater = min(self.storeWater,self.consCleanWater)
        self.consStoreWater = min(self.consStoreWater,self.storeWater)
        print("inside updateVals")
        print(self.unCleanWater)
        print(self.consUnCleanWater)

        print("inside update function dict" )
        print(self.countProjects)

    def processNotifs(self,notif) :
        if notif == "Drought" : 
            for x in self.JSONdict["offsetsFromRegular"]["Rain"] : 
                self.offSets[x] = self.JSONdict["offsetsFromRegular"]["Rain"][x]
        elif notif == "Summer" : 
            for x in self.JSONdict["offsetsFromRegular"]["Rain"] : 
                self.offSets[x] = self.JSONdict["offsetsFromRegular"]["Rain"][x]
        elif notif == "Rain" :
            for x in self.JSONdict["offsetsFromRegular"]["Rain"] : 
                self.offSets[x] = self.JSONdict["offsetsFromRegular"]["Rain"][x]

        elif notif == "Flood" :
            pass

        elif notif == "Tourists" :

            pass

        elif notif == "Reset" : 
            for proj,changes in self.offSets.items() : 
                self.offSets[proj] = 0  

