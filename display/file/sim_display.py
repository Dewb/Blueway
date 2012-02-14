#!/usr/bin/env python

#from numpy import shape,zeros,minimum,maximum,ravel;
import sys

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
<canvas id="myCanvas" width="%d" height="%d" style="border:1px solid #c3c3c3;background:black;">
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
class FileScreen:
   def setup_screen(self,dimensions,locations):
      self.dims = dimensions
      self.locs = locations
      print "setting up dimensions: "+str(self.dims)
      self.HTML_HEAD_FILLED = HTML_HEAD%(self.dims[2]+100,self.dims[3])
   def render(self,pixels):
           #sys.stdout.write("printing LEDs.html\n")
           f=open("LEDs.html", "w")
           out=self.HTML_HEAD_FILLED
           for i in range(len(self.locs)):
              x,y = self.locs[i]
              col= pixels[i]
              hexcolor = '#%02x%02x%02x'%(col[0],col[1],col[2])
              out+=""" 
ctx.fillStyle="%s";
ctx.beginPath();
ctx.arc(%d,%d,2,0,Math.PI*2,true);
ctx.closePath();
ctx.fill();""" % (hexcolor, x, y)
           out+=HTML_FOOT
           f.write(out)
           f.close()
