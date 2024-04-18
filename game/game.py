import pygame as pg
from .gameWorldAlt import GameData
from .util import drawDebugText,isoCoordToRenderPos,isoRenderPosToImgRenderPos,changeOfBasis,basisVecX,basisVecY
from .settings import TILE_SIZE
from .powerManagement import PowerManagement
from .waterManagement import WaterManagement
from .camera import Camera

import sys
import pygame_gui 
from game.mainGameUI import MainGameUI
from pygame import Rect
from pygame_gui.elements.ui_button import UIButton
from .audio import AudioManager
from .groundRender import GroundRender
from .renderTreeRock import RockTreeRender
"""
def cameraMovement(width,height):
    mouse_pos = pg.mouse.get_pos()
    fractionY = 0.03 
    fractionX = 0.03
    dx = 0
    dy = 0
    speed = 25
    if mouse_pos[0] > width*(1-fractionX):
        dx = speed
    elif mouse_pos[0] < width*fractionX:
        dx = -speed
    
    if mouse_pos[1] > height*(1-fractionY):
        dy = speed
    elif mouse_pos[1] < height*fractionY:
        dy = -speed
    
    return (dx,dy)
"""
def cameraMovement(width,height):
    return (0,0)
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
    __slot__ = ["screen","clock","width","height","world","playing","cameraPos","centreOffset","groundBuffSize","firstRender","manager","mainGameGUI","clearButton","appendButton","groundCenterOffset","imgCenterOffset","powerManagement","renderTreeRock","uiEnable"]
    def __init__(self,screen,clock):
        self.screen = screen 
        self.clock = clock
        self.width,self.height = self.screen.get_size()
        # self.allProjectsList = []

        self.powerManagement = PowerManagement(self)        
        self.waterManagement = WaterManagement(self)

        self.audioManager = AudioManager()
        self.audioManager.playMusic()
        self.manager = pygame_gui.UIManager((self.width,self.height))
        self.mainGameUI = MainGameUI(self.manager,"./res/json/theme.json",self)
        self.world = GameData(50,50,self.width,self.height,self,
                              "res/graphics/imgForPlacement/mapWaterGrasscopy.png",
                              "res/graphics/imgForPlacement/mapWaterGrasscopy2.png")
        self.playing = True

        self.camera = Camera()
        #
        self.groundBuffSize = self.calGroundSurfaceSize()
        self.centerOffset = self.calCenterOffset(self.groundBuffSize[0],self.groundBuffSize[1])

        imgOffsetX = (self.width - self.groundBuffSize[0])/2
        imgOffsetY = (self.height - self.groundBuffSize[1])/2
        self.imgCenterOffset =(imgOffsetX,imgOffsetY)
        #self.groundSurface = pg.Surface(self.groundBuffSize).convert_alpha()
        #self.firstRender = True
        self.groundRender = GroundRender(self.camera,self.groundBuffSize,self.centerOffset,self.imgCenterOffset,self.world)



        self.loadFonts()

        self.clearButton = UIButton(Rect(500,500,100,50),"Clear HTML",self.manager)
        self.appendButton = UIButton(Rect(600,600,100,50),"Append HTML",self.manager)
        self.appendingTxt = """<br>
        <b>Simple test</b>
        </br>
        """
        self.timeDelta = self.clock.tick(60)/1000.0
        self.groundCenterOffset = self.centerOffset

        self.renderTreeRock = RockTreeRender(self.camera,self.centerOffset,self.world,self.imgCenterOffset)
        self.uiEnable = True

    def loadFonts(self):
        self.manager.add_font_paths("Montserrat",
                                    "./res/fonts/Montserrat-Regular.ttf",
                                    "./res/fonts/Montserrat-Bold.ttf",
                                    "./res/fonts/Montserrat-Italic.ttf",
                                    "./res/fonts/Montserrat-BoldItalic.ttf")
        self.manager.preload_fonts([
            {'name':'Montserrat','html_size':'6','style':'bold'},
            {'name':'Montserrat','html_size':'4','style':'regular'}
        ])
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
        self.world.writeRockTreeData("playerData.png","maintData.txt")
        pg.quit()
        sys.exit()
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
        if keys[pg.K_z]:
            self.uiEnable = False
        # print("list og events" , pg.event.get())
        eventslist = pg.event.get()
        # (pg.event.get().reverse)
        eventslist.reverse()
        buttonClicked = False
        for event in eventslist:
            # print(templist)
            if event.type == pg.QUIT:
                self.quitScene()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quitScene()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                buttonClicked = True
                self.audioManager.playSound("click")
                if event.ui_element == self.clearButton:
                    self.mainGameUI.notificationBox.clearHtmlText()
                if event.ui_element == self.appendButton:
                    self.mainGameUI.notificationBox.appendHtmlText(self.appendingTxt)
                self.mainGameUI.processEvents(event,self.audioManager,self.world)

            elif event.type == pg.MOUSEBUTTONDOWN and buttonClicked == False:
                mouseX,mouseY = pg.mouse.get_pos()
                coordinates = self.mainGameUI.projectUIWrapper.projectListWindow.rect
                pos = self.findClickCoord(mouseX,mouseY)
                (posX,posY) = pos

                if not(mouseX < coordinates[0] or mouseX > coordinates[0]+coordinates[2] or mouseY < coordinates[1] or mouseY > coordinates[1]+coordinates[3]):
                    pass
                else : 
                # self.world.rockTreeData[posX][posY] = {"tile":self.world.imgIndxMap["building01"]} 
                    projName = self.mainGameUI.projectUIWrapper.clickedOnWorld(posX,posY)
                    #add set stats function to powerManagement
                    if projName != None:
                        self.powerManagement.handleProj(projName)
                    if projName != None:
                        self.audioManager.playSound("construction")
                        # self.game.allProjectsList.append()
                        self.waterManagement.handleProj(projName)   
                      
            self.manager.process_events(event)
            
        #perhaps next statement outside loop recheck later
        self.manager.update(self.timeDelta)
    def update(self):
        (dx,dy) = cameraMovement(self.width,self.height)
        self.camera.moveCamera(dx,dy)
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
        # for x in range(self.world.noBlockX-1,-1,-1):
            for y in range(self.world.noBlockY-1,-1,-1):
            # for y in range(self.world.noBlockY):    
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
        #self.drawGround()
        self.groundRender.drawGround(self.screen)
        fps = round(self.clock.get_fps())
        #print("fps is:",fps)
        self.renderTreeRock.drawTreeRock(self.screen)
        self.renderTreeRock.drawPlacementReq(self.mainGameUI.projectUIWrapper.curTileDrawReq,self.screen)
        drawDebugText(self.screen,"fps={}".format(fps),(255,255,255),(550,550))

        if self.uiEnable:
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
    
