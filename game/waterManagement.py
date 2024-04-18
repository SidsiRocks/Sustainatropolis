from typing import Any
import json
from .statisticsUI import StatisticsWindow
from .MessageWindow import MessageWindow
from pygame import Rect
from pygame_gui.core import ObjectID

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
        self.regular = findDict["regular"]
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
        self.population = 0
        self.currentlyDown = findDict["currentlyDown"] 
        self.game = game
    def getScore(self) :
        print("self.population" , self.population)
        return self.population

    def decreaseMaintenance(self) :
        for proj in self.game.world.allProjectsList :
            print(proj) 
            proj.decMaintenance(10)
            if proj.maintenance == 0 :
                proj.maintenance = 0
                proj.maintBar.set_current_progress(0)
            # pass
            

    def createNotEnoughWindow(self,manager,warnWinMessHTML):
        width = 300
        height = 300
        winWidth = manager.window_resolution[0]
        winHeight = manager.window_resolution[1]
        wanrWinRect = Rect((winWidth-width)/2,(winHeight-height)/2,width,height)
        
        buttonHt = 50
        buttonWdth = 100
        paddingY = 10
        paddingX = 15
        warnWindow = MessageWindow(wanrWinRect,warnWinMessHTML,buttonHt,
                                   buttonWdth,paddingY,paddingX,manager,
                                   "Not Enough Money",
                                   ObjectID(class_id="@warnWindow",object_id="#warnWindow"),1)
        return warnWindow
    
    
    def waterDataTplValid(self,tpl):
        pass
    

    def validProjPlace(self,manager,projName):
        print(projName)
        print("inside validProjPlace function")
        if projName == "Purification Plant" : 
            if self.unCleanWater < self.consUnCleanWater + self.regular[projName] : 
            # render warning
                print("Came here")
                self.game.mainGameUI.projectUIWrapper.createNotEnoughWindow("Warning! \n Right Now, You're not having enough unclean water supply that you case use to purify.")
                #self.createNotEnoughWindow(manager,"Warning! \n Right Now, You're not having enough unclean water supply that you case use to purify.")
        if projName == "WaterTank" :
            if self.cleanWater < self.consCleanWater + self.regular[projName] :
                self.createNotEnoughWindow(manager,"Warning! \n Right Now, You're not having enough clean water supply that you case use to store.")
        if projName == "CityBuilding" : 
                self.game.mainGameUI.projectUIWrapper.createNotEnoughWindow("Warning! \n Right Now, You're not having enough clean water supply that you case use to store.")
                #self.createNotEnoughWindow(manager,"Warning! \n Right Now, You're not having enough clean water supply that you case use to store.")
        if projName == "CityBuilding1" : 
            if self.storeWater < self.consStoreWater + self.regular[projName] :
                self.game.mainGameUI.projectUIWrapper.createNotEnoughWindow("Warning! \n Right Now, You're not having enough stored water supply that you can supply to increase population.")
                #self.createNotEnoughWindow(manager,"Warning! \n Right Now, You're not having enough stored water supply that you can supply to increase population.")
    def setStats(self,statWin:StatisticsWindow):
        statWin.setStats("Unclean Water",self.consUnCleanWater,self.unCleanWater)
        statWin.setStats("Clean Water",self.consCleanWater,self.cleanWater)
        statWin.setStats("Store Water",self.consStoreWater,self.storeWater)
        statWin.setStats("Sewage Water",self.consSewageWater,self.sewageWater)

    def handleProj(self,project) :
        print(project)
        if project in self.countProjects :
            self.countProjects[project] += 1
        else : 
            self.countProjects[project] = 1
        # if project == "purificationPlant" and self.unCleanWater < self.consUnCleanWater: 
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
        self.population = 0 
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
                print("here inside consume store water")
                self.consStoreWater += (self.JSONdict["consumeStoreWater"][proj] + self.offSets[proj] ) * self.countProjects[proj]
                self.population += 100*self.countProjects[proj]
                print("self.population",self.population)
                print(self.countProjects[proj])
                print(proj )
                print(self.countProjects)
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

