import time
import brickpi3 as BP
import grovepi as GROVE

LEGO = BP.BrickPi3()

#note port 3 is

##
#[A, B, C, D]
#[1 ------ 4]
#[2 ------ 3]
#[power]

LEGO_ITEMS = {
    "MOTOR_LEFT": LEGO.PORT_A,
    "MOTOR_RIGHT": LEGO.PORT_D,
    "EV3_GYRO": LEGO.PORT_3,
    
}



DELAY = .02
PWR = 15
WHEEL_DIA_M = 0.05556504



X_AXIS = (1,0)
ORIGIN = (0,0)
###CHANGE AS NEEDED FOR THE POC POINT TO POINT MOVE
##THE 4 POINTS TO NAVIGATE TO
GRID_SIZE_CONVERSION = 1 #conversion from units to meters ie units * GRID_SIZE_CONVERSION = meters
POINT1 = (4,4)
POINT2 = (2, 3)
POINT3 = (-1, -2)
POINT4 = (4, 4)
