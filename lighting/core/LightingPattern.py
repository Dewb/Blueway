import time

class LightingPattern(object):
    duration = 10
    end = False

    def __init__(self, args):
        if len(args) > 0: self.duration = float(args[0])

    def display_pattern(self,t):
        raise NotImplementedError

    def illuminate(self):
        self.end = False
        t0 = time.time()
        t = time.time()
        while t < t0 + self.duration and not self.end:
            self.display_pattern(t)
            t = time.time()

    def stop(self):
        self.end = True
