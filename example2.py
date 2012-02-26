#!/usr/bin/env python
# above line for unix only

# imports 
import optparse, time, sys, colorsys
from numpy import ones, zeros, array
from time import sleep

from display.route_display import *
from light_matrix import *

# configuration options for how the display command is routed may be found
# in config/__init__.py  DEFAULT file-based rendering will be deprecated soon

OFF = [0,0,0]
CYAN = [0,1,1]
MAGENTA = [1,0,1]
YELLOW = [1,1,0]
ON = [1,1,1]

def main():
     incr, loopStart, delay = getCommandLineOptions()

     # initialize a display at full white (1.0)
     lights = LightMatrix(route_display, 1.0) 
     
     # send values to the lights/simulator for a count of 2 seconds
     # to give the browser time to open, etc.
     print "initializing..."
     for i in range(2):
          lights.display()
          sleep(1)
     print "...done init()"
     
     # set up an array to cycle through colors
     colors = [CYAN, MAGENTA, YELLOW, OFF, ON]
     colorIndex = 0

     loopCount = loopStart # default 0

     # loop forever until ctrl-c is pressed
     while 1:
          # loop over all columns of the lights, assigning the new value
          while loopCount < lights.cols and loopCount >= loopStart:
               lights.display()
               lights.setColumnRGB(loopCount, colors[colorIndex])
               sleep(delay/1000.) # sleep takes seconds
               loopCount += incr

          # After getting up to 50 or down to -1, increment the colorIndex.
          colorIndex += 1
          # The modulo operator "%" says take the remainder of a division, so
          # colorIndex will count: 0,1,2,3,4,0,1,2,3,4 since len(colors) == 5 .
          colorIndex = colorIndex % len(colors)
          
          # Reverse the direction of pattern movement.
          incr = -incr 
          
          #ensure the loopCount index remains in the actual lights
          loopCount = max(min(loopCount,lights.cols-1),0)



def getCommandLineOptions():
     """ interprets and returns script-specific options"""
     parser = optparse.OptionParser(usage="%prog [options] incrementor")
     parser.add_option("--delay", action="store", type="int", help="set delay in milliseconds for each loop")
     parser.add_option("--start", action="store", type="int", help="which channel to start the incrementor at")
     (opts, args) = parser.parse_args()
     if len(args) != 1:
          parser.error("incorrect number of arguments")     
     msDelay = opts.delay or 100 # in milliseconds
     incr = int(args[0])
          
     loopStart = opts.start or 0  #opts.start will be "None" if not specified
     
     return incr, loopStart, msDelay

if __name__ == '__main__':
     main()
