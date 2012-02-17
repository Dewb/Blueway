#!/usr/bin/env python

import socket
import sys
from display import colormap
from random import random as randomF
from numpy import zeros,array
from config import Ds
# best when canvas w(1000), h(200) are divisible by size[2], size[3]

def make_sockets(Ds):
    return range(len(Ds))
 
def make_locs(sockets):
    x_space = 10
    y_space = 10
    offset=[10,10]
    between_chains = 13

    locs = []
    x=0
    y=0
    for j in range(len(sockets)):
        for chan in [1,2]:
            for i in range(50):
                x=offset[0]+i*x_space
                y=offset[1]+(chan-1)*y_space + j*(between_chains)
                locs.append([x,y])
    return locs

def floatToIntColor(rgb):
    a=(rgb*255+.5).round()
    a[a>255] = 255
    a[a<0] = 0
    return a

def randomBrightColor():
    hue = randomF()
    sat = randomF()/2.0 + .5
    val = 1.0
    hue, sat, val = colorsys.hsv_to_rgb(hue, sat, val)
    ret = array([hue, sat, val])
    return floatToIntColor(ret)

def randomDimColor(value):
    hue = randomF()
    sat = randomF()/2.0 + .5
    val = value
    hue, sat, val = colorsys.hsv_to_rgb(hue, sat, val)
    ret = array([hue, sat, val])
    return floatToIntColor(ret)    
    

def display(data, sock, chan=1):
   return floatToIntColor(data).reshape(50,3)

def displayi(data,sock,chan=1,CM=colormap.MATLAB_COLORMAP):
   return display(colormap.i2c(data,CM),sock,chan)

def imdisplay(data,socks,mapping,screen):
   sz = len(socks);
   px = zeros([100*sz,3])
   for i in range(0,sz):
     p=display(data[:,mapping[2*i]-1],socks[i],1)
     px[i*50:i*50+50,:]=p
     p=display(data[:,mapping[2*i+1]-1],socks[i],2)
     px[i*50+100:i*50+150,:]=p
   screen.render(px)

def imdisplayi(data,socks,mapping,screen,CM=colormap.MATLAB_COLORMAP):
    sz = len(socks);
    px = zeros([100*sz,3])
    for i in range(0,sz):
      p=displayi(data[:,mapping[2*i]-1],socks[i],1,CM)
      px[i*50:i*50+50,:]=p
      p=displayi(data[:,mapping[2*i+1]-1],socks[i],2,CM)
      px[i*50+100:i*50+150,:]=p
    screen.render(px)

