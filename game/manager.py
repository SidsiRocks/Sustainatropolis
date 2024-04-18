from .audio import AudioManager
from .game import MainGameScene
from .camera import Camera
from .gameWorldAlt import GameData
class Manager: 
    def __init__(self,screen,clock) :
        self.audioManager = AudioManager()
        self.camera = Camera()
        self.game = MainGameScene(screen,clock,self)
