import pygame as pg
from .gameWorldAlt import GameData
from .util import drawDebugText,isoCoordToRenderPos,isoRenderPosToImgRenderPos,changeOfBasis,basisVecX,basisVecY
from .settings import TILE_SIZE
from .waterManagement import WaterManagement
from .camera import Camera

import json
import pygame_gui 
from game.mainGameUI import MainGameUI
from pygame import Rect
from .audio import AudioManager
from .groundRender import GroundRender
from .renderTreeRock import RockTreeRender
from .onCloseButtonEvent import OnCloseWindowButton
from .Project import Project
from pygame_gui.core import ObjectID

def cameraMovementKeyBoard(keyPress):
    speed = 25
    if keyPress == pg.K_w:
        return (0,-speed)
    elif keyPress == pg.K_s:
        return (0,speed)
    elif keyPress == pg.K_d:
        return (speed,0)
    elif keyPress == pg.K_a:
        return (-speed,0)




class MainGameScene:
    def __init__(self,screen,clock,turnBarFilePath,moneyFilePath,writeMaintFilePath,mapDataFilePath):
        self.screen = screen 
        self.clock = clock
        self.width,self.height = self.screen.get_size()


        self.waterManagement = WaterManagement(self)

        self.audioManager = AudioManager()
        self.audioManager.playMusic()
        self.manager = pygame_gui.UIManager((self.width,self.height))
        self.loadFonts()
        self.mainGameUI = MainGameUI(self.manager,"./res/json/theme.json",self,turnBarFilePath=turnBarFilePath,writeMaintFilePath=moneyFilePath)

        mapDataDict = json.load(open(mapDataFilePath))

        self.world = GameData(self.width,self.height,self,mapDataDict,writeMaintFilePath)
        self.playing = True

        self.camera = Camera()
        self.groundBuffSize = self.calGroundSurfaceSize()
        self.centerOffset = self.calCenterOffset(self.groundBuffSize[0],self.groundBuffSize[1])

        imgOffsetX = (self.width - self.groundBuffSize[0])/2
        imgOffsetY = (self.height - self.groundBuffSize[1])/2
        self.imgCenterOffset =(imgOffsetX,imgOffsetY)
        self.groundRender = GroundRender(self.camera,self.groundBuffSize,self.centerOffset,self.imgCenterOffset,self.world)




        self.timeDelta = self.clock.tick(60)/1000.0
        self.groundCenterOffset = self.centerOffset

        self.renderTreeRock = RockTreeRender(self.camera,self.centerOffset,self.world,self.imgCenterOffset)
    
        onCloseFunc = lambda: self.quitScene()
        onCloseButtonFunc = lambda: (self.mainGameUI.maintManager.setMaintAllowed(True),self.mainGameUI.projectUIWrapper.setProjAllowed(True))
        closeWinWidth,closeWinHeight = 400,300
        closeWindowRect = Rect((self.width - closeWinWidth)/2,(self.height -closeWinHeight)/2,
                            closeWinWidth,closeWinHeight)
        closeWinMsg = f"""<font face='Montserrat' color="#ffffff" size=4.5>
Are you sure you want to quit the game?</font>"""
        self.closeWindow = OnCloseWindowButton(closeWindowRect,
                        closeWinMsg,80,120,10,10,self.manager,
                        "Exit Game?",object_id=ObjectID("#closeWindow","@closeWindow"),
                        onCloseFunc=onCloseFunc,draggable=False,
                        buttonMsg = "Exit",visible=0,onCloseButtonFunc=onCloseButtonFunc)
        self.mainGameUI.turnBar.proceedEvent("Welcome" , self.mainGameUI)
    def loadFonts(self):
        self.manager.add_font_paths("Montserrat",
                                    "./res/fonts/Montserrat-Regular.ttf",
                                    "./res/fonts/Montserrat-Bold.ttf",
                                    "./res/fonts/Montserrat-Italic.ttf",
                                    "./res/fonts/Montserrat-BoldItalic.ttf")
        self.manager.preload_fonts(json.load(open("res/json/fontsDictionary.json")))
    def run(self):
        
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
    def calCenterOffset(self,width,height):
        offX = -(self.world.noBlockX + self.world.noBlockY)*TILE_SIZE/2+ width/2
        offY = -(self.world.noBlockX - self.world.noBlockY)*TILE_SIZE/4 + height/2
        return (offX,offY)
    def quitScene(self):
        turnBarFilePath = "game/currentStartGame/turnBarYear.txt"
        moneyFilePath = "game/currentStartGame/money.txt"
        writeMaintFilePath = "game/currentStartGame/writeMaint.txt"
        mapDataFilePath = "game/currentStartGame/mapData.json"
        

        self.world.writeRockTreeData(mapDataFilePath,writeMaintFilePath)
        self.mainGameUI.turnBar.writeTurnBarUI(turnBarFilePath)
        self.mainGameUI.notificationBox.writeMoney(moneyFilePath)

        self.playing = False
        print("Scene must be quit now")
    def stopPlaying(self):
        print("Game playing set to false")
        self.playing = False
    def mouseHoverEvents(self):
        x,y = pg.mouse.get_pos()
        isoX,isoY = self.findClickCoord(x,y)
        #print(f"hover on coordinates {isoX} {isoY}")
        self.mainGameUI.projectUIWrapper.hoverOnWorld(isoX,isoY)
    def events(self):
        self.timeDelta = self.clock.tick(60)/1000.0
        keys = pg.key.get_pressed()
        self.mouseHoverEvents()
        if keys[pg.K_w]:
            x,y = cameraMovementKeyBoard(pg.K_w)
            self.camera.moveCamera(x,y)
        if keys[pg.K_a]:
            x,y = cameraMovementKeyBoard(pg.K_a)
            self.camera.moveCamera(x,y)
        if keys[pg.K_s]:
            x,y = cameraMovementKeyBoard(pg.K_s)
            self.camera.moveCamera(x,y)
        if keys[pg.K_d]:
            x,y = cameraMovementKeyBoard(pg.K_d)
            self.camera.moveCamera(x,y)
        if keys[pg.K_p] : 
            self.audioManager.toggleMusic()
        if keys[pg.K_KP_PLUS] : 
            self.audioManager.setVolume(self.audioManager.getVolume()+0.1)
        if keys[pg.K_KP_MINUS] :
            self.audioManager.setVolume(self.audioManager.getVolume()-0.1)
        if keys[pg.K_q]:
            self.audioManager.playSound("test")
        eventslist = pg.event.get()
        eventslist.reverse()
        for event in eventslist:
            if event.type == pg.QUIT:
                self.quitScene()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mainGameUI.maintManager.setMaintAllowed(False)
                    self.mainGameUI.projectUIWrapper.setProjAllowed(False)
                    self.closeWindow.show()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.mainGameUI.processEvents(event,self.audioManager,self.world)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseX,mouseY = pg.mouse.get_pos()
                coordinates = self.mainGameUI.projectUIWrapper.projectListWindow.rect
                pos = self.findClickCoord(mouseX,mouseY)
                (posX,posY) = pos

                if not(mouseX < coordinates[0] or mouseX > coordinates[0]+coordinates[2] or mouseY < coordinates[1] or mouseY > coordinates[1]+coordinates[3]):
                    pass
                else : 
                    projName = self.mainGameUI.projectUIWrapper.clickedOnWorld(posX,posY)
                    if projName != None:
                        self.audioManager.playSound("construction")
                        self.waterManagement.handleProj(projName)   
                    
                    curDrawReq = self.mainGameUI.projectUIWrapper.curTileDrawReq
                    if type(curDrawReq) != Project:
                        self.mainGameUI.maintManager.handleClick(posX,posY)
            self.manager.process_events(event)
            
        self.manager.update(self.timeDelta)
    def update(self):
        self.mainGameUI.update()
        totalOffset = self.renderTreeRock.calTotalOffset()
        self.world.updateProjMaintBar(totalOffset)
    def drawToGroundBuff(self):
        groundImgArr = self.world.imgArr
        groundData = self.world.groundData
        centerOffset = self.centerOffset
        self.groundCenterOffset = centerOffset

        for x in range(self.world.noBlockX):
            for y in range(self.world.noBlockY-1,-1,-1):
                renderPos = isoCoordToRenderPos((x,y),centerOffset)
                curImg = groundImgArr[groundData[x][y]["tile"]]
                #print("x:",x,"y:",y,"renderPos:",renderPos)
                self.groundSurface.blit(curImg,renderPos)
    def drawTreeRock(self):
        centerOffset = self.centerOffset
        totalCenterOffset = (centerOffset[0]+self.imgCenterOffset[0]-self.camera.getX()
                             ,centerOffset[1]+self.imgCenterOffset[1]-self.camera.getY())
        rockTreeData = self.world.rockTreeData
        groundImgArr = self.world.imgArr
        offsetArr = self.world.offsetArr
        for x in range(self.world.noBlockX):
            for y in range(self.world.noBlockY-1,-1,-1):
                curDict =  rockTreeData[x][y]
                if type(curDict) == dict:
                    renderPos = isoCoordToRenderPos((x,y),totalCenterOffset)
                    tileName = curDict["tile"]
                    curImg = groundImgArr[tileName]
                    curOff = offsetArr[tileName]
                    imgRenderPos = isoRenderPosToImgRenderPos(renderPos,curImg.get_width(),curImg.get_height())
                    imgRenderPos = (imgRenderPos[0]+curOff[0],imgRenderPos[1]+curOff[1])
                    self.screen.blit(curImg,imgRenderPos)
    def calGroundSurfaceSize(self):
        width  = (self.world.noBlockX + self.world.noBlockY)*TILE_SIZE
        height = ((self.world.noBlockX + self.world.noBlockY)*TILE_SIZE)//2 + 4*TILE_SIZE
        return (width,height)
    def draw(self):
        self.screen.fill((0,0,0))
        self.groundRender.drawGround(self.screen)
        fps = round(self.clock.get_fps())
        self.renderTreeRock.drawTreeRock(self.screen)
        self.renderTreeRock.drawPlacementReq(self.mainGameUI.projectUIWrapper.curTileDrawReq,self.screen)
        drawDebugText(self.screen,"FPS={}".format(fps),(255,255,255),(350,10))

        self.manager.draw_ui(self.screen)

        pg.display.flip()
    def findIsoGridOrg(self):
        orgX = self.imgCenterOffset[0] - self.camera.getX() + isoCoordToRenderPos((0,0),self.groundCenterOffset)[0]+0
        orgY = self.imgCenterOffset[1] - self.camera.getY() + isoCoordToRenderPos((0,0),self.groundCenterOffset)[1]+TILE_SIZE/2
        return (orgX,orgY)
    def findClickCoord(self,mouseX,mouseY):
        (orgX,orgY) = self.findIsoGridOrg()
        xRel = mouseX - orgX
        yRel = mouseY - orgY
        (X,Y) = changeOfBasis((xRel,yRel),basisVecX(),basisVecY())
        return (int(X),int(Y))
    
