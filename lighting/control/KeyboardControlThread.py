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
    "exit": General.exit,
    "debug": General.debug,
    "list": General.list
}

class KeyboardControlThread(ControlThread):
    patterns = [x[0] for x in CODE_WORDS.iteritems() if x[1].__module__.startswith('lighting.patterns')]
    def acceptable_command(self, command):
        return CODE_WORDS.has_key(command.strip('/'))

    def deny_command(self, command):
        print command + " does not match any registered pattern"

    def perform_command(self, command, args):
        function = CODE_WORDS.get(command)
        if function.__module__.startswith('lighting.patterns'):
            self.lighting_thread.swap_current_pattern(function(args))
        elif function.__module__.startswith('lighting.control'):
            try:
                function(args,self)
            except TypeError as e:
                print e.message
        else:
            print "you so crazy!"

    def get_input(self):
        choice =  sys.stdin.readline().split()
        while not choice:
            choice =  sys.stdin.readline().split()
        return choice

