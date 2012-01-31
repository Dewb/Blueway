#!/usr/bin/env python

import socket
import sys
import colormap;
from numpy import shape,zeros,minimum,maximum,ravel;

import web_server
s=WebScreen(opts,args)
x_space = 24
y_space = 24

def make_sockets(Ds):
    return range(len(Ds))

def display(data, sock, chan=1):
   locs = []
   pixels = []
   for i in range(50):
      (r,g,b)=data[i*3:(i*3+3)]
      x=i*x_space+sock*(50*xspace)
      y=(chan-1)*y_space
      locs.append([x,y])
      pixels.append((r,g,b))
   setup_screen([0,0,x,y],locs,pixels)   
      # def display(data, sock, chan=1):
      #    xmit = zeros(174, 'ubyte')
      #    xmit[:8], xmit[20:24] = [4, 1, 220, 74, 1, 0, 8, 1], [150, 0, 255, 15]
      #    xmit[16], xmit[24:] = chan, minimum(maximum(256 * ravel(data), 0), 255)
      #    sock.sendall(xmit)

def displayi(data,sock,chan=1,CM=colormap.MATLAB_COLORMAP):
   display(colormap.i2c(data,CM),sock,chan)

def imdisplay(data,socks,mapping):
   sz = len(socks);
   for i in range(0,sz):
     display(data[:,mapping[2*i]-1],socks[i],1)
     display(data[:,mapping[2*i+1]-1],socks[i],2)

def imdisplayi(data,socks,mapping,CM=colormap.MATLAB_COLORMAP):
   sz = len(socks);
   for i in range(0,sz):
     displayi(data[:,mapping[2*i]-1],socks[i],1,CM)
     displayi(data[:,mapping[2*i+1]-1],socks[i],2,CM)


 def teh_displayi(data,CM=colormap.MATLAB_COLORMAP):
 	imdisplayi(data,sockets,mapping,CM);

 def teh_display(data):
 	imdisplay(data,sockets,mapping);



