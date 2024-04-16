from typing import Any
import json
from .statisticsUI import StatisticsWindow

class WaterManagement:

    def __init__ (self) :
<<<<<<< HEAD
        findDict = json.load(open("res/json/waterManagement.json"))
=======
        # self.statsManager = StatisticsWindow()
        findDict = json.load(open("game/waterManagement.json"))
        self.JSONdict = findDict
>>>>>>> Test
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
    # def handleProj(self,projName):
    #     unCleanWaterTpl,cleanWaterTpl,storeWaterTpl,sewageWaterTpl = self.updateVal(projName)
        
    #     self.unCleanWater,self.consUnCleanWater = unCleanWaterTpl
    #     self.cleanWater,self.consCleanWater = cleanWaterTpl
    #     self.storeWater,self.consStoreWater = storeWaterTpl
    #     self.sewageWater,self.consSewageWater = sewageWaterTpl

    # def updateVal(self,projName):
    #     unCleanWater,consUnCleanWater = self.unCleanWater,self.consUnCleanWater
    #     cleanWater,consCleanWater = self.cleanWater,self.consCleanWater
    #     storeWater,consStoreWater = self.storeWater,self.consStoreWater
    #     sewageWater,consSewageWater = self.sewageWater,self.consSewageWater

    #     if projName in self.prodUncleanWater:
    #         unCleanWater = unCleanWater + self.prodUncleanWater[projName]
    #     if projName in self.consUncleanWaterDic:
    #         consUnCleanWater = consUnCleanWater + self.consUncleanWaterDic[projName]

    #     if projName in self.prodCleanWater:
    #         cleanWater = cleanWater + self.prodCleanWater[projName]
    #     if projName in self.consCleanWaterDic:
    #         consCleanWater = consCleanWater + self.consCleanWaterDic[projName]

    #     if projName in self.prodStoreWater:
    #         storeWater = storeWater + self.prodStoreWater[projName]
    #     if projName in self.consStoreWaterDic:
    #         consStoreWater = consStoreWater + self.consStoreWaterDic[projName]     
    
    #     if projName in self.prodSewage:
    #         sewageWater = sewageWater + self.prodSewage[projName]
    #     if projName in self.consSewageDic:
    #         consSewageWater = consSewageWater + self.consSewageDic[projName]        

    #     unCleanWaterTpl = (unCleanWater,consUnCleanWater)
    #     cleanWaterTpl = (cleanWater,consCleanWater)
    #     storeWaterTpl = (storeWater,consStoreWater)
    #     sewageWaterTpl = (sewageWater,consSewageWater)

    #     return (unCleanWaterTpl,cleanWaterTpl,storeWaterTpl,sewageWaterTpl)

    def waterDataTplValid(self,tpl):
        unCleanWaterTpl,cleanWaterTpl,storeWaterTpl,sewageWaterTpl = tpl
        
        isValidUnClean =  unCleanWaterTpl[0] >= unCleanWaterTpl[1]
        isValidClean   =  cleanWaterTpl[0] >= cleanWaterTpl[1]
        isValidSewage = sewageWaterTpl[0] >= sewageWaterTpl[1]
        isValidStore = storeWaterTpl[0] >= sewageWaterTpl[1]

        if not isValidUnClean:
            return ("unclean water",(unCleanWaterTpl))
        if not isValidClean:
            return ("clean water",(cleanWaterTpl))
        if not isValidSewage:
            return ("sewage",(sewageWaterTpl))
        if not isValidStore:
            return ("store water",(storeWaterTpl))
        return None
    
    def validProjPlace(self,projName):
        self.updateVals()
        # Updates the values 

        return self.waterDataTplValid(self.updateVal(projName))

    def setStats(self,statWin:StatisticsWindow):
        statWin.setStats("unclean water",self.consUnCleanWater,self.unCleanWater)
        statWin.setStats("clean water",self.consCleanWater,self.cleanWater)
        statWin.setStats("store water",self.consStoreWater,self.storeWater)
        statWin.setStats("sewage water",self.consSewageWater,self.sewageWater)

    def projectPlanted(self,project) :
        print("planting project" , project)
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
        print("inside updateVals")
        print(self.unCleanWater)
        print(self.consUnCleanWater)

        print("inside update function dict" )
        print(self.countProjects)

    def processNotifs(self,notif) :
        if notif == "drought" : 
            print("drough came inside water Management")
            self.offSets["Dam"] = -5
            self.offSets["waterPump"] = -7
            self.updateVals()
        elif notif == "summer" : 
            self.offSets["Dam"] = -10
            self.offSets["waterPump"] = -5
            self.offSets["CityBuilding1"] = 5
            self.offSets["CityBuilding2"] = 5
        
        elif notif == "reset" : 
            for proj,changes in self.offSets.items() : 
                self.offSets[proj] = 0  

