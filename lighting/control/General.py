__author__ = 'mDan'

import sys
from lighting.display.web.web_display import screen

def help(args,state):
  print state
def exit(args,control_thread):
  control_thread.lighting_thread.stop()
  control_thread.stop()
  screen.web_sock.do_SIGINT(None,None)
  sys.exit(0)
