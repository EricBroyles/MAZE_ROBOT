from constants import LEGO, ORIGIN, POINT1, POINT2, POINT3, POINT4, Y_AXIS
from config import configLEGO
from control import goToPoint, pause, move
from map import getMap

print("Config Sensors Running")
configLEGO()
points = [(0,4), (-1,4), (2,4)]
try:
    prev_pt = (0,0)
    for pt in points:
        prev_pt = goToPoint(prev_pt, pt)

    map = getMap([(0,0)] + points)
    print(map)

    # print("starting")
    # pt1 = goToPoint(ORIGIN, POINT1)
    # pause()
    # pt2 = goToPoint(pt1, POINT2)
    # pause()
    # pt3 = goToPoint(pt2, POINT3)
    # pause()
    # pt4 = goToPoint(pt3, POINT4)
    
    print("done -> hit ctrl + c")

except KeyboardInterrupt:
    print("stopping")
    LEGO.reset_all()

