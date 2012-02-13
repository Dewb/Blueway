from config import CONFIG

if CONFIG.web:
    if CONFIG.file:
	    from file.web_display import *
    else:
        from web.web_display import *
else:
	from display import *

	Ds = ['3','4','5','6','12','13','14','36','19','20','15','16']
	mapping = [11,10,7,5,2,1,3,4,13,16,15,14,9,12,8,6,24,23,21,22,18,20,17,19]
	sockets = make_sockets(Ds)

	def route_displayi(data,CM=colormap.MATLAB_COLORMAP):
		imdisplayi(data,sockets,mapping,CM)

	def route_display(data):
		imdisplay(data,sockets,mapping)

