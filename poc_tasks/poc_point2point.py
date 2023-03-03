from constants import LEGO, ORIGIN, POINT1, POINT2, POINT3, POINT4
from config import configLEGO
from control import goToPoint, pause

print("Config Sensors Running")
configLEGO()
    
try:
    print("starting")
    pt1 = goToPoint(ORIGIN, POINT1)
    pause()
    #nned to run a pause command
    pt2 = goToPoint(pt1, POINT2)
    pause()
    pt3 = goToPoint(pt2, POINT3)
    pause()
    pt4 = goToPoint(pt3, POINT4)
    print("done -> hit ctrl + c")

except KeyboardInterrupt:
    print("stopping")
    LEGO.reset_all()