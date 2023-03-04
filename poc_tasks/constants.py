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


#Robot assumes it is facing the pos x-axis
Y_AXIS = (0,1)
ORIGIN = (0,0)
###CHANGE AS NEEDED FOR THE POC POINT TO POINT MOVE
##THE 4 POINTS TO NAVIGATE TO

#ex 1 grid size unit is 1 ft, so grid conversion should be .305
#ex 1 grid size unit is 1 m, so gird conversion should be 1
GRID_SIZE_CONVERSION = .305 #conversion from units to meters ie units * GRID_SIZE_CONVERSION = meters
POINT1 = (1,1)
POINT2 = (1, 1)
POINT3 = (2,2)
POINT4 = (0, 0)
