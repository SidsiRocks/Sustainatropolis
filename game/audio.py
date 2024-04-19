from pygame import mixer 


class AudioManager : 
    def __init__ (self) : 
        mixer.init()
        self.sounds = {}
        self.music = None
        self.musicPlaying = False
        self.loadMusic("res/music/music.mp3")
        print(self.getVolume())
        self.volume = 1
        self.setVolume(1)
        self.loadSound("test","res/music/sound.mp3")
        self.loadSound("construction","res/audios/construction.wav")
        self.loadSound("click","res/audios/audio.mp3")
        self.loadSound("celebration","res/audios/celebration.wav")
        self.loadSound("maintenance","res/audios/maintenance.mp3")
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
        if self.volume != volume:
            mixer.music.set_volume(volume)
            for sound in self.sounds:
                self.sounds[sound].set_volume(volume)
        self.volume = volume
    def getVolume(self):
        return mixer.music.get_volume()
    def stopAll(self):
        mixer.stop()
        self.musicPlaying = False
        self.music = None
        self.sounds = {}

    