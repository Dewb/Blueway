from config import CONFIG
import pygame
from pygame.locals import Color
#import pdb
from numpy import maximum,minimum
import util.TimeOps as timeops

class GameScreen:
    size = []
    locs = []
    pixels = []
    scale = None
    def __init__(self):
        pygame.init()    

    def setup_screen(self,size,locs):
        self.size = size
        self.locs = locs
        #size = (1000, 200)
        self.screen = pygame.display.set_mode(size[2:])
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(Color(0,0,0))
        self.stopwatch = timeops.Stopwatch()
        self.stopwatch.start()

    def render(self, px=None, currentTime=timeops.time()):
        if px != None:
            self.pixels = px    
        if self.scale:
            scale = self.scale
        else:
            scale = 1
        for i in range(len(self.locs)):
            loc = self.locs[i]
            value = self.pixels[i]
            if not(all(value == (0,0,0))):
            	pygame.draw.circle(self.background, value, loc*scale, scale)
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
        self.stopwatch.stop()
        pygame.display.set_caption("fps: "+str(int(1000/self.stopwatch.elapsed())))
        self.stopwatch.start()
