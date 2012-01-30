#!/usr/bin/env python
# encoding: utf-8
"""
test_websock.py

Created by Daniel Taub on 2012-01-29.
Copyright (c) 2012 CEMMI. All rights reserved.
"""

#from operationscore.Renderer import *
#import util.TimeOps as timeops
#import util.ComponentRegistry as compReg
import colormap;
import time as clock;
from numpy import shape,zeros,minimum,maximum,ravel,array;
import threading, socket, re, struct, hashlib, json, sys
import optparse, colorsys, random,webbrowser, select, os
from itertools import izip
from SocketServer import ThreadingMixIn
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from websocket import WebSocketServer

queue = []
queueLock = threading.Lock()

def randomLoc(maxBoundingBox, minBoundingBox=(0,0)): #TODO: make less shitty
    loc = []
    loc.append(random.randint(minBoundingBox[0], maxBoundingBox[0]))
    loc.append(random.randint(minBoundingBox[1], maxBoundingBox[1]))
    return tuple(loc)
    
    
def floatToIntColor(rgb):
    rgb[0] = int(rgb[0]*256 + .5)
    rgb[1] = int(rgb[1]*256 + .5)
    rgb[2] = int(rgb[2]*256 + .5)
    return safeColor(rgb)

def safeColor(c):
    """Ensures that a color is valid"""
    c[0] = c[0] if c[0] < 255 else 255
    c[1] = c[1] if c[1] < 255 else 255
    c[2] = c[2] if c[2] < 255 else 255
    return c

    
def randomBrightColor():
    hue = random.random()
    sat = random.random()/2.0 + .5
    val = 1.0
    hue, sat, val = colorsys.hsv_to_rgb(hue, sat, val)
    ret = [hue, sat, val]
    return array(floatToIntColor(ret))

def randomDimColor(value):
    hue = random.random()
    sat = random.random()/2.0 + .5
    val = value
    hue, sat, val = colorsys.hsv_to_rgb(hue, sat, val)
    ret = [hue, sat, val]
    return floatToIntColor(ret)    
    
    
class Screen:
    size = []
    locs = []
    pixels = []
    def __len__(self):
        return len(self.locs)
    def __iter__(self): # iterator over all pixels
        return izip(self.locs, self.pixels)
    def __init__(self):
        self.size = [0,0,796,210]
        self.locs = [[196, 60] ,[192, 60] ,[188, 60] ,[184, 60] ,[180, 60] ,[176, 60] ,[172, 60],
                    [168, 60] ,[164, 60] ,[160, 60] ,[156, 60] ,[152, 60] ,[148, 60] ,[144, 60],
                    [140, 60] ,[136, 60] ,[132, 60]]
        
        #self.locs = [(0,0),(10,10),(20,20)]0
        self.pixels = [randomBrightColor() for i in self.locs]
        #self.pixels = [array(x) for x in [(2, 0, 60),(2, 0, 76),(2, 0, 83),(2, 0, 76),(2, 0, 60),(1, 0, 40),(0, 0, 0),
#                       (35, 9, 0),(60, 16, 0),(90, 24, 0),(115, 31, 0),(161, 47, 0),(161, 48, 0), (141, 43, 0),
#                       (107, 33, 0),(71, 23, 0),(0, 0, 0)]]
SCREEN=Screen()
print SCREEN.pixels

class WebSocketRenderer(WebSocketServer):
    """
    WebSockets server that echos back whatever is received from the
    client.  
    """
    buffer_size = 8096

    def new_client(self):
        """
        Echo back whatever is received.
        """

        cqueue = []
        c_pend = 0
        cpartial = ""
        rlist = [self.client]

        while True:
            wlist = []

            if cqueue or c_pend: wlist.append(self.client)
            ins, outs, excepts = select.select(rlist, wlist, [], 1)
            if excepts: raise Exception("Socket exception")

            if self.client in outs:
                # Send queued target data to the client
                c_pend = self.send_frames(cqueue)
                cqueue = []

            if self.client in ins:
                # Receive client data, decode it, and send it back
                frames, closed = self.recv_frames()
                cqueue.extend(["You said: " + f for f in frames])

                if closed:
                    self.send_close()
                    raise self.EClose(closed)


class RenderThread():
    """Renders frame data over a websocket.
        Port: Websocket listen port
    """
    def __init__(self,server):
	self.SocketServer = server
        self.connection_thread = threading.Thread(target=self.handle_renders)
        self.connection_thread.daemon = True
        self.connection_thread.start()

    def handle_renders(self):
        while True:
            self.render(SCREEN,clock.time())
            clock.sleep(1)
    
    def render(self, lightSystem, currentTime=clock.time()*1000):
        json_frame = [0]*len(lightSystem)
        i = 0
        for (loc, c) in lightSystem:
            if all(c < 0.05):
                continue
            cs = 'rgb({0},{1},{2})'.format(*c)
            json_frame[i] = (map(int, loc), cs)
            i += 1

        json_frame = json_frame[0:i]
        size = SCREEN.size
        
        json_data = json.dumps(dict(status='ok', size=map(int, size), frame=json_frame))
#        self.client_push(json_data)
# ************* here we do server-side push!
        
    def client_push(self, data):
        dead_clients = []
        for i in range(len(self.clients)):
            try:
                self.server.send_frames(data)
                #clients[i].send("\x00")
                #self.clients[i].send(data)
                #self.clients[i].send("\xff")
            except socket.error:
                dead_clients.append(i)
        
        for i in range(len(dead_clients)):
            self.close_sock(self.clients[dead_clients[i]-i])
            del self.clients[dead_clients[i]-i]
        self.clients_lock.release()
    

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass
class SimpleWebserver(ThreadingHTTPServer): 
    def __init__(self,hostname,port):
	self.server = ThreadingHTTPServer((hostname,int(port)),MyHandler)
	print 'started httpserver...'
        server_thread = threading.Thread(target=self.run)
        server_thread.daemon = True
        server_thread.start()
        # 
        #     def sensingLoop(self):
    def run(self):
        running = True
        try:
            while running:
                self.server.handle_request() # blocks until request 
        except KeyboardInterrupt:
            print '^C received, shutting down server'
            self.server.socket.close()
        finally:
            print 'Shutting down server'
            self.server.socket.close()


class MyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def wwrite(self,data,line_break = None):
        if line_break != None:
            self.wfile.write(data + line_break) # could be <br> or \n
        else:
            self.wfile.write(data)
    def tag(self, text, tag = 'html'):
        return "<{0}>{1}</{0}>".format(tag,text)
 
    def hwrite(self,data):
        self.wwrite(self.tag(data),None)
    def do_GET(self):
        wwrite=self.wwrite
        hwrite=self.hwrite
        try:
            if self.path.startswith("/static/"):
		f = open(self.path[8:],"r")
                self.send_response(200)
                self.send_header('Content-type','text/html; charset=utf-8')
                self.end_headers() 
                self.wfile.write(f.read())
		f.close()
            elif self.path.strip('/') == '':
                self.send_response(301)
                self.send_header('Location','/static/index.html')
                self.end_headers()
            else:
                self.send_response(404)
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     ## in case post is needed, use the following (from Jon Berg , turtlemeat.com)
     #
     # def do_POST(self):
     #     global rootnode
     #     try:
     #         ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
     #         if ctype == 'multipart/form-data':
     #             query=cgi.parse_multipart(self.rfile, pdict)
     #         self.send_response(301)
             
     #         self.end_headers()
     #         upfilecontent = query.get('upfile')
     #         print "filecontent", upfilecontent[0]
     #         self.wfile.write("<HTML>POST OK.<BR><BR>");
     #         self.wfile.write(upfilecontent[0]);
             
     #     except :
     #         pass


if __name__ == '__main__':
  
    parser = optparse.OptionParser(usage="%prog [options] [listen_port]")
    parser.add_option("--verbose", "-v", action="store_true",
            help="verbose messages and per frame traffic")
    parser.add_option("--cert", default="self.pem",
            help="SSL certificate file")
    parser.add_option("--key", default=None,
            help="SSL key file (if separate from cert)")
    parser.add_option("--ssl-only", action="store_true",
            help="disallow non-encrypted connections")
    (opts, args) = parser.parse_args()
    hostname = 'localhost'
    port = '8080'
    
    if len(args) == 0:
       opts.listen_port = 8000
    else:
       opts.listen_port = int(args[0])

    opts.web = './static/'  #changes directory to here
    print opts.__dict__
    
    w=WebSocketRenderer(**opts.__dict__)
    r=RenderThread(w)
    s=SimpleWebserver(hostname,port)
    #webbrowser.open('http://'+hostname+':'+str(port))
    w.start_server()
