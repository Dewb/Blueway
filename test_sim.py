import sim_display as display
from numpy import zeros
from time import sleep

data=zeros([150])
for i in range(50):
    data[(3*i) : (3*i+3)]=255
    #print data
    sockets=display.make_sockets(["36"])
    display.display(data,sockets[0])
    sleep(1)

