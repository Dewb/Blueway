import sys
from ControlThread import ControlThread
from lighting.patterns import *
import General

CODE_WORDS = {
    "color": Color, #
    "cgl1" : CGL1, #
    "cgl2" : CGL2,
    "quadratic" : Quadratic, #
    "blue" : BlueCord, #
    "twinkle" : TwinklePlusPlus, #
    "cruft" : Cruft, #
    "seq" : Sequence,
    "help": General.help,
    "exit": General.exit
}

class KeyboardControlThread(ControlThread):
    def acceptable_command(self, command):
        return CODE_WORDS.has_key(command.strip('/'))

    def deny_command(self, command):
        print command + " does not match any registered pattern"

    def perform_command(self, command, args):
        function = CODE_WORDS.get(command)
	if function.__module__.startswith('lighting.patterns'):
	       	super.lighting_thread.swap_current_pattern(function(args))
	elif function.__module__.startswith('lighting.control'):
		try:
			function(args,self)
		except Exception as e:
			print e
	else:
		print "you so crazy!"

    def get_input(self):
	choice =  sys.stdin.readline().split()
	while choice != []:
		choice =  sys.stdin.readline().split()
        return choice

