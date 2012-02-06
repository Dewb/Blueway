#!/usr/bin/env python

import socket
import sys
from display import colormap
from random import random as randomF
from numpy import shape,zeros,minimum,maximum,ravel,array,ones

import web_server
import webbrowser

#webbrowser.open('http://localhost:8000/')

screen=web_server.WebScreen()
x_space = 10
y_space = 10
offset=[10,10]
between_chains = 13

def make_sockets(Ds):
    return range(len(Ds))

Ds = ['3','4']#,'5','6','12','13','14','36','19','20','15','16'];
mapping = [11,10,7,5,2,1,3,4,13,16,15,14,9,12,8,6,24,23,21,22,18,20,17,19];
sockets = make_sockets(Ds);

locs = []
x=0
y=0
for j in range(len(sockets)):
    for chan in [1,2]:
        for i in range(50):
            x=offset[0]+i*x_space
            y=offset[1]+(chan-1)*y_space + j*(between_chains)
            locs.append([x,y])

screen.setup_screen([0,0,500,50],locs)
# best when canvas w(1000), h(200) are divisible by size[2], size[3]

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

def imdisplay(data,socks,mapping):
   sz = len(socks);
   px = zeros([100*sz,3])
   for i in range(0,sz):
     p=display(data[:,i],socks[i],1)
     px[i*50:i*50+50,:]=p
     p=display(data[:,i+1],socks[i],2)
     px[i*50+100:i*50+150,:]=p
   screen.render(px)
   

def imdisplayi(data,socks,mapping,CM=colormap.MATLAB_COLORMAP):
    sz = len(socks);
    px = zeros([100*sz,3])
    for i in range(0,sz):
      p=displayi(data[:,i],socks[i],1,CM)
      px[i*50:i*50+50,:]=p
      p=displayi(data[:,i+1],socks[i],2,CM)
      px[i*50+100:i*50+150,:]=p
#      s.setup_screen([0,0,x_space*50*sz,y_space*2],lc)   
    screen.render(px)

     
def route_displayi(data,CM=colormap.MATLAB_COLORMAP):
 	imdisplayi(data,sockets,mapping,CM);

def route_display(data):
 	imdisplay(data,sockets,mapping);



