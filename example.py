#!/usr/bin/env python
# above line for unix only

import optparse, time, sys
from display.route_display import *
from numpy import ones, zeros

if __name__ == '__main__':
	parser = optparse.OptionParser(usage="%prog [options] incrementor")
	parser.add_option("--delay", action="store", type="int", help="set delay in milliseconds for each loop")
	parser.add_option("--start", action="store", type="int", help="which channel to start the incrementor at")
	(opts, args) = parser.parse_args()
	if len(args) != 1:
		parser.error("incorrect number of arguments")	

	incrementor = int(args[0])
	loopCount = opts.start or 0  #opts.start will be "None" if not specified

	data = ones([150,4])*255
	while loopCount < 150:
		route_display(data)
		time.sleep((opts.delay or 500)/1000.)
		data[loopCount] = 0 
		loopCount += incrementor
	print 'done'
	sys.exit(0)
