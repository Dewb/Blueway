#!/usr/bin/env python
# encoding: utf-8
"""
web_server.py

Created by Daniel Taub on 2012-01-29.
Copyright (c) 2012 CEMMI. All rights reserved.
"""

#from operationscore.Renderer import *
#import util.TimeOps as timeops
#import util.ComponentRegistry as compReg
import time as clock;
from numpy import shape,zeros,minimum,maximum,ravel,array, random;
import threading, socket, re, struct, hashlib, json, sys
import optparse, colorsys,select, os
from itertools import izip
from SocketServer import ThreadingMixIn
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from websocket import WebSocketServer
from multiprocessing import Queue
from Queue import Empty
from lighting.config import CONFIG

class WebScreen:
    size = []
    locs = []
    pixels = []
    updated = False
    dummy = False
    def __len__(self):
        return len(self.locs)
    def __iter__(self): # iterator over all pixels
        return izip(self.locs, self.pixels)
        
    def __init__(self,opts={'cert': 'self.pem', 'verbose': None, 'key': None, 'ssl_only': None},
                      args=[]):
        hostname = 'localhost'
        port = '8080'
        
        if len(args) == 0:
           opts['listen_port'] = CONFIG.listen_port
        else:
           opts['listen_port'] = int(args[0])

        opts['web'] = os.path.dirname(__file__)+'/static/'
#        opts['web'] = './static/'  #serves files from this dir on 8000!
        
        #magick happens here:
        self.web_sock=WebSocketRenderer(self,opts)
        # this can go away eventually?
        #self.page_serve=SimpleWebserver(hostname,port)
        #webbrowser.open('http://'+hostname+':'+str(port))

    def setup_dummy_screen(self):
        self.size = [0,0,796,210]
        self.locs = [[196, 60] ,[192, 60] ,[188, 60] ,[184, 60] ,[180, 60] ,[176, 60] ,[172, 60],
                            [168, 60] ,[164, 60] ,[160, 60] ,[156, 60] ,[152, 60] ,[148, 60] ,[144, 60],
                            [140, 60] ,[136, 60] ,[132, 60]]
        self.locs.extend([[196, 40] ,[192, 40] ,[188, 40] ,[184, 40] ,[180, 40] ,[176, 40] ,[172, 40],
                                                    [168, 40] ,[164, 40] ,[160, 40] ,[156, 40] ,[152, 40] ,[148, 40] ,[144, 40],
                                                    [140, 40] ,[136, 40] ,[132, 40]])
        self.dummy = True
    def update_dummy_screen(self):
        self.update([random.random_integers(0,255,3) for i in self.locs])
        self.updated = True

    def update(self,px):
        self.pixels = px
        self.updated = True

    def setup_screen(self,size,locs):
        self.size = map(int,size)
        self.locs = locs

    def render(self,px=None):
        if self.dummy:
            self.update_dummy_screen()
        if not self.updated:
            return
   
        currentTime=clock.time()*1000
        json_frame = [0]*len(self)
        i = 0

        for (loc, c) in self:
            if all(c < 0.05):
                cs = '000000'
            cs = '#%02x%02x%02x' % (c[0],c[1],c[2])
            #cs = 'rgb({0},{1},{2})'.format(*c)
            #cs = 'rgb('+str(int(c[0]))+','+str(int(c[1]))+','+str(int(c[2]))+')'
            json_frame[i] = (loc, cs)
            i += 1
        status = 'ok'
        self.send_json(status,self.size,json_frame)
        
    def setup(self):
        json_frame = self.locs
        status = 'setup'
        self.send_json(status,self.size,json_frame)
        
    def send_json(self,status,size,json_frame):

        json_data = json.dumps(dict(status=status, size=size, frame=json_frame))
        #self.client_push(json_data)
        self.web_sock.send_all(json_data)


class WebSocketRenderer(WebSocketServer):
    """
    WebSockets server that echos back whatever is received from the
    client.  
    """
    buffer_size = 8096
    def __init__(self,screen,args):
        self.screen = screen
        WebSocketServer.__init__(self,**args)
    def main_loop_callback(self):
        self.screen.render()
        
    def send_all(self,data):
        toremove = []
	#print len(self.queues)
        for i in range(len(self.queues)):
            q,active =self.queues[i]
            qmode = active.value
            if qmode == 1:
                try:
                    q.put(data)
                except IOError:
                    toremove.append(i)
            elif qmode == 0:
                toremove.append(i)
            elif qmode == 2:
                pass
            else:
                sys.exit(0)
                print "shouldn't happen"
               
        for i in range(len(toremove)):
            del self.queues[toremove[i]-i]
        
    def new_client(self, (gqueue,active)):
        """
        Echo back whatever is received.
        """
        self.screen.setup()
        cqueue = []
        c_pend = 0
        cpartial = ""
        rlist = [self.client]

        while active.value != -1:
            try:
                next = gqueue.get(False)
                cqueue.append(next)
            except Empty:
                pass
            except Exception:
                _, exc, _ = sys.exc_info()
                self.msg("queue read exception: %s" % str(exc))
                
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
                    active.value = 0 
                    self.send_close()
                    raise self.EClose(closed)

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
    
    s=WebScreen(opts.__dict__,args)
    s.setup_dummy_screen()
    s.web_sock.start_server()
    
