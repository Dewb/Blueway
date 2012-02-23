from config import CONFIG
import pygame
#from pygame.locals import *si
#import pdb
from numpy import maximum,minimum

class GameScreen:
    size = []
    locs = []
    pixels = []
    
    def __init__():
        pygame.init()    

    def setup_screen(self,size,locs):
        self.size = size
        self.locs = locs
        #size = (1000, 200)
        self.screen = pygame.display.set_mode(size[2:])
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(Color(0,0,0))
#        self.stopwatch = timeops.Stopwatch()
#        self.stopwatch.start()

    def render(self, px=None):
        if px != None:
            self.pixels = px
        #self.blit?



class PygameRenderer(Renderer):
    """PygameRenderer is a renderer which renders the LightSystem to a pygame display"""
    
    def render(self, lightSystem, currentTime=timeops.time()):
        self.background.fill(Color(0,0,0))
        if 'Scale' in self:
            scale = self['Scale']
        else:
            scale = 1

        for loc, value in lightSystem:
	    if not(all(value == (0,0,0))):
            	pygame.draw.circle(self.background, value, loc*scale, scale)
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
        self.stopwatch.stop()
        pygame.display.set_caption(str(int(1000/self.stopwatch.elapsed())))
        self.stopwatch.start()
