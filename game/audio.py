from pygame import mixer 


class AudioManager : 
    def __init__ (self) : 
        mixer.init()
        self.sounds = {}
        self.music = None
        self.musicPlaying = False
<<<<<<< HEAD
        self.loadMusic("res/music/music.mp3")
        print(self.getVolume())
        self.loadSound("click","res/music/sound.mp3")
=======
        self.loadMusic("game/music.mp3")
        self.loadSound("click","game/sound.mp3")
>>>>>>> Test
    def loadSound(self,soundName,soundPath):
        self.sounds[soundName] = mixer.Sound(soundPath)
    def playSound(self,soundName):
        self.sounds[soundName].play()
    def loadMusic(self,musicPath):
        self.music = musicPath
    def playMusic(self):
        mixer.music.load(self.music)
        mixer.music.play(1)
        self.musicPlaying = True
    def stopMusic(self):
        mixer.music.stop()
        self.musicPlaying = False
    def pauseMusic(self):
        mixer.music.pause()
        self.musicPlaying = False
    def unpauseMusic(self):
        mixer.music.unpause()
        self.musicPlaying = True
    def isMusicPlaying(self):
        return self.musicPlaying
    def toggleMusic(self):
        if self.musicPlaying:
            self.pauseMusic()
        else:
            self.unpauseMusic()
    def setVolume(self,volume):
        if(volume > 1 or volume < 0):
            return 
        mixer.music.set_volume(volume)
        for sound in self.sounds:
            self.sounds[sound].set_volume(volume)
    def getVolume(self):
        return mixer.music.get_volume()
    def stopAll(self):
        mixer.stop()
        self.musicPlaying = False
        self.music = None
        self.sounds = {}

    