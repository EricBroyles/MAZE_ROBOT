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
