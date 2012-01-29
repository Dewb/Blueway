#!/usr/bin/env python

import socket
import sys
import threading, Queue
import colormap;
from numpy import shape,zeros,minimum,maximum,ravel;

HTML_HEAD = """
<head>
  <meta charset="utf-8">

  <!-- Use the .htaccess and remove these lines to avoid edge case issues.
       More info: h5bp.com/b/378 -->
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title></title>
  <meta name="description" content="">
  <meta name="author" content="">

  <!-- Mobile viewport optimized: j.mp/bplateviewport -->
  <meta name="viewport" content="width=device-width,initial-scale=1">

  <!-- Place favicon.ico and apple-touch-icon.png in the root directory: mathiasbynens.be/notes/touch-icons -->

  <!-- 
  <link rel="stylesheet" href="css/style.css">
  -->

<META HTTP-EQUIV="Refresh" CONTENT="1">
</head>

<body>

  <div id="container">
    <header>

    </header>
    <div id="main" role="main">
<canvas id="myCanvas" width="195" height="345" style="border:1px solid #c3c3c3;">
Your browser does not support the canvas element.
</canvas>

<script type="text/javascript">
var c=document.getElementById("myCanvas");
var ctx=c.getContext("2d");
"""
HTML_FOOT = """
</script> 
    </div>
    <footer>

    </footer>
  </div> <!--! end of #container -->


  <!-- JavaScript at the bottom for fast page loading -->

  <!-- Grab Google CDN's jQuery, with a protocol relative URL; fall back to local if offline -->
  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"></script>
  <script>window.jQuery || document.write('<script src="js/libs/jquery-1.6.2.min.js"><\/script>')</script>


  <!-- scripts concatenated and minified via ant build script-->
  <script defer src="js/plugins.js"></script>
  <script defer src="js/script.js"></script>
  <!-- end scripts-->

	
  <!-- Change UA-XXXXX-X to be your site's ID -->
  <script>
    window._gaq = [['_setAccount','UAXXXXXXXX1'],['_trackPageview'],['_trackPageLoadTime']];
    Modernizr.load({
      load: ('https:' == location.protocol ? '//ssl' : '//www') + '.google-analytics.com/ga.js'
    });
  </script>


  <!-- Prompt IE 6 users to install Chrome Frame. Remove this if you want to support IE 6.
       chromium.org/developers/how-tos/chrome-frame-getting-started -->
  <!--[if lt IE 7 ]>
    <script src="//ajax.googleapis.com/ajax/libs/chrome-frame/1.0.3/CFInstall.min.js"></script>
    <script>window.attachEvent('onload',function(){CFInstall.check({mode:'overlay'})})</script>
  <![endif]-->
  
</body>
</html>"""

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


