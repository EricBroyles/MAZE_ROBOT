from constants import LEGO, ORIGIN, Y_AXIS
from config import configLEGO
from control import goToPoint, pause, move

print("Config Sensors Running")
configLEGO()

GRID_SIZE_CONVERSION = .46 #conversion from units to meters ie units * GRID_SIZE_CONVERSION = meters
POINT1 = (1,2)
POINT2 = (3, 3)
POINT3 = (4,0)
POINT4 = (1, 4) #basically the origin with no zero error
    
try:
    print("starting")
    pt1 = goToPoint(ORIGIN, POINT1)
    # pt2 = goToPoint(pt1, POINT2)
    # pt3 = goToPoint(pt2, POINT3)
    # pt4 = goToPoint(pt3, POINT4)
    
    print("done -> hit ctrl + c")

except KeyboardInterrupt:
    print("stopping")
    LEGO.reset_all()
