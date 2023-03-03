import time
import numpy as np
from math import pi

import brickpi3 as BP
import grovepi as GROVE


LEGO = BP.BrickPi3()

###CHANGE AS NEEDED FOR THE POC
UNITS = "METRIC"
X_AXIS = (1,0)
ORIGIN = (0,0)
##THE 4 POINTS TO NAVIGATE TO
GRID_SIZE = 1 #conversion from units to meters ie units * GRID_SIZE = meters
POINT1 = (4,4)
POINT2 = (2, 3)
POINT3 = (-1, -2)
POINT4 = (4, 4)


LEFT_MOTOR = BP.Port_A
RIGHT_MOTOR = BP.Port_D
GYRO_PORT = BP.Port_3
DELAY = .02
PWR = 40
WHEEL_DIA_M = 0.05556504

LEGO.set_sensor_type(GYRO_PORT, LEGO.SENSOR_TYPE.EV3_GYRO_ABS)
print("config sensor")
time.sleep(3)
print("done config sensor -> test val: ", LEGO.get_sensor(GYRO_PORT))

def turn(direction, degree):

    initRotation = LEGO.get_sensor(GYRO_PORT)[0]

    if(direction == "RIGHT"):
        #left goes forward
        #right goes backward
        LEGO.set_motor_power(LEFT_MOTOR, PWR)
        LEGO.set_motor_power(RIGHT_MOTOR, -PWR)
    else:
        #left goes backward
        #right goes forward
        LEGO.set_motor_power(LEFT_MOTOR, -PWR)
        LEGO.set_motor_power(RIGHT_MOTOR, PWR)
    
    currRotation = LEGO.get_sensor(GYRO_PORT)[0]
    delta = abs(degree)

    print("\033[94m BEGIN @turn: currRotation =", currRotation, " vs initRotation = ", initRotation)
    while(abs(currRotation) - abs(initRotation) < delta):
        time.sleep(DELAY)
        currRotation = LEGO.get_sensor(GYRO_PORT)[0]
        print("\033[92m @turn: currRotation =", currRotation, " vs initRotation = ", initRotation)

    print("\033[1m END @turn: currRotation =", currRotation, " vs initRotation = ", initRotation)  
    
    LEGO.set_motor_power(LEFT_MOTOR, 0)
    LEGO.set_motor_power(RIGHT_MOTOR, 0)
def move(distance):

    currLeftMotorEncoder = LEGO.get_motor_encoder(LEFT_MOTOR)
    
    LEGO.offset_motor_encoder(currLeftMotorEncoder)

    finalEncoderVal = 360 * (distance / (pi * WHEEL_DIA_M))

    LEGO.set_motor_power(LEFT_MOTOR, PWR)
    LEGO.set_motor_power(RIGHT_MOTOR, PWR)

    while(abs(currLeftMotorEncoder) <= finalEncoderVal):
        time.sleep(DELAY)
        currLeftMotorEncoder = LEGO.get_motor_encoder(LEFT_MOTOR)
    
    LEGO.set_motor_power(LEFT_MOTOR, 0)
    LEGO.set_motor_power(RIGHT_MOTOR, 0)


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in degrees between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    radian = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    return radian * (180 / pi)

def findDirection():

    currRotation = abs(LEGO.get_sensor(GYRO_PORT)[0])

    ###DRAW A LINE WITH LENGHT = 1 at the given angle, then if the x component is 
    ###greater than the y it is closer to the x
    ### if it is neg or positive means if it points in the neg or pos direction
    


##ASSUMES the robot is placed in the pos x direction
def goToPoint(fromPt, toPt):

    xMove = toPt[0] - fromPt[0]
    yMove = toPt[1] - fromPt[1]

    distance = pow((GRID_SIZE * xMove)**2 + (GRID_SIZE * yMove)**2,.5)
    targetAngle = angle_between(X_AXIS, (xMove, yMove))
    currRotation = LEGO.get_sensor(GYRO_PORT)[0]

    turnAngle = targetAngle - currRotation

    turn("LEFT", turnAngle)

    move(distance)




    # #move the x movement

    # #if the x movement is pos go in pos x dir -> position robot on the pos x gyro is 0, 360, -360,  etc


    # currRotation = LEGO.get_sensor(GYRO_PORT)[0]
    # if(not(currRotation % 360 == 0)):
    #     #find the difference between the current rotation and the nearest multiple of 360
    #     #and turn that amount 
    #     difference = currRotation % 360

    #     #cw ie right
    #     if(difference < 0):
    #         turn("RIGHT", difference)
    #     else:
    #         turn("LEFT", difference)



    return toPt


def pause():
    LEGO.set_motor_power(LEFT_MOTOR, 0)
    LEGO.set_motor_power(RIGHT_MOTOR, 0)
    print("PAUSING")
    go = input("enter anything to start again: ")
    
    



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