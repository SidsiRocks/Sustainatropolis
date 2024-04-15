

from typing import Any


class WaterManagemetSystem :

    def __init__ (self) :
        self.nDams = 1
        self.nBores = 1
        self.nReserviors = 1
        self.nWaterPurificationPlants = 1
        self.uncleanWaterPerDam = 100
        self.uncleanWaterPerBore = 50
        self.cleanWaterPerReservior = 200
        self.cleanWaterPerPurificationPlant = 150
    def getUncleanWater(self) :
        return self.nDams * self.uncleanWaterPerDam + self.nBores * self.uncleanWaterPerBore
    
    def getCleanWater(self) :
        ans = 0
        for reserviors in self.waterStoragesDict["reserviors"] :
            ans += reserviors[1]
        return ans
    
    def addDam(self) :
        self.nDams += 1        
    def addBore(self) :
        self.nBores += 1
    def addReservior(self) :
        self.nReserviors += 1
    def addPurificationPlant(self) :
        self.nWaterPurificationPlants += 1
    
