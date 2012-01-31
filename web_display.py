#!/usr/bin/env python

import socket
import sys
import colormap;
from numpy import shape,zeros,minimum,maximum,ravel,array

import web_server
s=web_server.WebScreen()
x_space = 10
y_space = 10
between_chains = 13
def make_sockets(Ds):
    return range(len(Ds))

Ds = ['3','4','5','6','12']#,'13','14','36','19','20','15','16'];
mapping = [11,10,7,5,2,1,3,4,13,16,15,14,9,12,8,6,24,23,21,22,18,20,17,19];
sockets = make_sockets(Ds);

locs = []
for j in range(len(sockets)):
    for i in range(50):
        for chan in [1,2]:
             x=100+i*x_space
             y=10+(chan-1)*y_space + j*(between_chains)
             locs.append([x,y])

s.setup_screen([0,0,1000,200],locs)   

def display(data, sock, chan=1):
   pixels = zeros([50,3])
   for i in range(50):
      (r,g,b)=data[i*3:(i*3+3)]
      pixels[i,:]=web_server.floatToIntColor([r,g,b])
   return pixels
      # def display(data, sock, chan=1):
      #    xmit = zeros(174, 'ubyte')
      #    xmit[:8], xmit[20:24] = [4, 1, 220, 74, 1, 0, 8, 1], [150, 0, 255, 15]
      #    xmit[16], xmit[24:] = chan, minimum(maximum(256 * ravel(data), 0), 255)
      #    sock.sendall(xmit)

def displayi(data,sock,chan=1,CM=colormap.MATLAB_COLORMAP):
   return display(colormap.i2c(data,CM),sock,chan)

def imdisplay(data,socks,mapping):
   sz = len(socks);
   px = zeros([100*sz,3])
   for i in range(0,sz):
     p=display(data[:,i],socks[i],1)
     px[i*50:i*50+50,:]=p
     p=display(data[:,i+1],socks[i],2)
     px[i*50+50:i*50+100,:]=p
   s.render(px)

def imdisplayi(data,socks,mapping,CM=colormap.MATLAB_COLORMAP):
    sz = len(socks);
    px = zeros([100*sz,3])
    for i in range(0,sz):
      p=displayi(data[:,i],socks[i],1,CM)
      px[i*50:i*50+50,:]=p
      p=displayi(data[:,i+1],socks[i],2,CM)
      px[i*50+50:i*50+100,:]=p
#      s.setup_screen([0,0,x_space*50*sz,y_space*2],lc)   
    s.render(px)

     
def teh_displayi(data,CM=colormap.MATLAB_COLORMAP):
 	imdisplayi(data,sockets,mapping,CM);

def teh_display(data):
 	imdisplay(data,sockets,mapping);



