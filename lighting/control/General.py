__author__ = 'mDan'

import sys
from lighting.display.web.web_display import screen

def help(args,control_thread):
  print "on your own, sorry"
def exit(args,control_thread):
  control_thread.lighting_thread.stop()
  control_thread.stop()
  screen.web_sock.end = True
  sys.exit(0)
def debug(args,control_thread):
  print "entering debugger"
  import pdb; pdb.set_trace()
