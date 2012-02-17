__author__ = 'mDan'

class CONFIG:
     MODES = ["FILE","WEB","LIVE"]
     mode = 2 # 0=render to file,1=websocket, 2=live to lights
     fileRefresh = .5
     
     subnet='10.32.0.{0}'
     
     hostname = 'localhost'
     listen_port = '8000'
     @staticmethod
     def getMode():
          return CONFIG.MODES[CONFIG.mode]

N = 50
M = 24

dt = 0.005
mapping = [1,1,2,2]#,11,10,7,5,3,4,13,16,15,14,9,12,8,6,24,23,21,22,18,20,17,19]
Ds = ['12','13']#,'5','6','12','13','14','36','19','20','15','16']
