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
import threading, socket, re, struct, hashlib, json, sys, colorsys, random, web,webbrowser
from itertools import izip

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

class WebsocketRenderer():
    """Renders frame data over a websocket.
        Specify: Hostname -- the hostname of the webserver providing the containing page
        Page: Static page to serve (if using builtin webserver)
        SourcePort: Port from which static page is serverd
        Port: Websocket listen port
    """
    
    def __init__(self,Hostname,Page,SourcePort,Port):
        self.hostname =Hostname
        self.port = int(Port)
        
        if SourcePort != None:
            self.orig_port = int(SourcePort)
        else:
            self.orig_port = 8080
        
        self.clients = []
        self.clients_lock = threading.Lock()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
        self.sock.listen(1)
        
        self.connection_thread = threading.Thread(target=self.handle_connections)
        self.connection_thread.daemon = True
        self.connection_thread.start()
            
    def handle_connections(self):
        while True:
            client, addr = self.sock.accept()
            print 'Accepted websocket connection from %s' % str(addr)
            header = ''
            while not re.search("\r?\n\r?\n.{8}", header): # Receive headers + 8 bytes data
                header += client.recv(1024)
            
            key1 = re.search("Sec-WebSocket-Key1: (.*)$", header, re.M).group(1)
            key2 = re.search("Sec-WebSocket-Key2: (.*)$", header, re.M).group(1)

            data = header[-8:]

            key1n = int(re.sub("[^\d]", '', key1))
            key1ns = key1.count(' ')
            n1 = key1n // key1ns

            key2n = int(re.sub("[^\d]", '', key2))
            key2ns = key2.count(' ')
            n2 = key2n // key2ns

            s = struct.pack("!II", n1, n2) + data
            respkey = hashlib.md5(s).digest()
            
            if self.orig_port == 80:
                origin = 'http://'+self.hostname
            else:
                origin = 'http://'+self.hostname+':'+str(self.orig_port)
            
            resp = \
                "HTTP/1.1 101 Web Socket Protocol Handshake\r\n" + \
                "Upgrade: WebSocket\r\n" + \
                "Connection: Upgrade\r\n" + \
                "Sec-WebSocket-Origin:"+ origin + "\r\n" + \
                "Sec-WebSocket-Location: ws://"+self.hostname+":"+ \
                    str(self.port)+"/\r\n" + \
                "Sec-WebSocket-Protocol: ledweb\r\n\r\n" + \
                respkey + "\r\n"

            client.send(resp)
            self.clients_lock.acquire()
            self.clients.append(client)
            self.clients_lock.release()
    
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
        self.client_push(json_data)
        
    def client_push(self, data):
        self.clients_lock.acquire()
        dead_clients = []
        for i in range(len(self.clients)):
            try:
                self.clients[i].send("\x00")
                self.clients[i].send(data)
                self.clients[i].send("\xff")
            except socket.error:
                dead_clients.append(i)
        
        for i in range(len(dead_clients)):
            self.close_sock(self.clients[dead_clients[i]-i])
            del self.clients[dead_clients[i]-i]
        self.clients_lock.release()
    
    def close_sock(self, s):
        try:
            c.shutdown(socket.SHUT_RDWR)
            c.close()
        except Exception:
            pass


class WebHandler(object):
    def GET(self, action):
        if action == '':
            action = 'index.html'

        if not action.startswith('input/'):
            raise web.Found('/static/'+action)

        params = web.input()
        queueLock.acquire()
        queue.append((action, params))
        queueLock.release()

        return json.dumps(dict(success=True))

class Webserver: 
    def __init__(self,hostname,port):
        urls = ('/(.*)', 'WebHandler')
        env = globals()
        env['sys'].argv = []
        app = web.application(urls, env)

        server_thread = threading.Thread(target=app.run)
        server_thread.daemon = True
        server_thread.start()
        # 
        #     def sensingLoop(self):
        #         queueLock.acquire()
        #         inputs = []
        #         while len(queue) > 0:
        #             inputs.append(queue.pop())
        #         resp = dict(inputs=inputs)
        #         queueLock.release()
        # #        self.respond(resp)
        # 


if __name__ == '__main__':
    
    hostname = 'localhost'
    port = '8080'
    w=WebsocketRenderer(hostname,'index.html',port,8000)
    s=Webserver(hostname,port)
    #webbrowser.open('http://'+hostname+':'+str(port))

    while True:
        w.render(SCREEN,clock.time())
        clock.sleep(1)
    print 'done'
