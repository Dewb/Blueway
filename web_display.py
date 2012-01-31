#!/usr/bin/env python

import socket
import sys
import colormap;
from numpy import shape,zeros,minimum,maximum,ravel;

import web_server

def connect(ip, port=6038):
   print "you should not call this"
   sock = socket(AF_INET, SOCK_DGRAM, 0)
   sock.connect((ip, port))
   return sock

#def make_sockets(Ds):
#    return [connect('10.32.0.{0}'.format(i)) for i in Ds];
def make_sockets(Ds):
    return [0]
    print "I don't do anything"
    HOST, PORT = "localhost", 9999
    sys.stderr.write("Warning: Sim mode only accepts 1 ip address\n")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return [sock]

def display(data, sock, chan=1):
   sys.stdout.write("printing LEDs.html\n")
   f=open("LEDs.html", "w")
   f.write(HTML_HEAD)
   for i in range(50):
      (r,g,b)=data[i*3:(i*3+3)]
      x=30+30 * (i%5)
      y=30+30 * (i/5)
      hexcolor = '#%02x%02x%02x' % (r,g,b)
      f.write(""" 
ctx.fillStyle="%s";
ctx.beginPath();
ctx.arc(%d,%d,15,0,Math.PI*2,true);
ctx.closePath();
ctx.fill();""" % (hexcolor, x, y))
   f.write(HTML_FOOT)
   f.close()


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


