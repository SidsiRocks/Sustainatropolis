class Camera:
    def __init__(self):
        self.cameraPos = (0,0)
    def moveCamera(self,x,y):
        self.cameraPos = (self.cameraPos[0] + x,self.cameraPos[1] + y)
    def getX(self):
        return self.cameraPos[0]
    def getY(self):
        return self.cameraPos[1]