from config import CONFIG, mapping, Ds

if CONFIG.getMode() == "WEB":
    from web.web_display import *
elif CONFIG.getMode() == "FILE":
    from file.web_display import *
else:
     from display import *
     sockets = make_sockets(Ds)
     def route_displayi(data,CM=colormap.MATLAB_COLORMAP):
          imdisplayi(data,sockets,mapping,CM)
     def route_display(data):
          imdisplay(data,sockets,mapping)

