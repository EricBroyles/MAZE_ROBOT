import time
from math import pi
from constants import *
from helpers import angle_between

def turn(delta, pwr = PWR):

    initDegree = LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"])
    print("@turn: initDegree = ", initDegree)

    target = initDegree + delta
    currDegree = initDegree

    #begin to turn

    #go cw -> right
    if(delta < 0):
        LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], pwr)
        LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], -pwr)
        while(currDegree > target):
            time.sleep(DELAY / 2)
            currDegree = LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"])
            #print("currDegree ", currDegree)
        
    #go ccw -> left
    elif(delta > 0):
        LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], -pwr)
        LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], pwr)
        while(currDegree < target):
            time.sleep(DELAY / 2)
            currDegree = LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"])
            #print("currDegree ", currDegree)
    else:
        print("@turn ERROR !!!!! no turn by 0 degree")
        return 0

    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], 0)
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], 0)
    print("@turn: done with ROTATION: ", LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"]), " vs currDegree: ", currDegree, "with initDegree: ", initDegree)

def move(distance):

    currLeftMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"])
    
    LEGO.offset_motor_encoder(currLeftMotorEncoder)

    finalEncoderVal = 360 * (distance / (pi * WHEEL_DIA_M))

    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], PWR)
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], PWR)

    while(abs(currLeftMotorEncoder) <= finalEncoderVal):
        time.sleep(DELAY)
        currLeftMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"])
    
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], 0)
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], 0)

def pause():
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], 0)
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], 0)
    print("PAUSING")
    go = input("enter anything to start again: ")
    return go

def goToPoint(fromPt, toPt):

    xMove = toPt[0] - fromPt[0]
    yMove = toPt[1] - fromPt[1]

    distance = pow((GRID_SIZE_CONVERSION * xMove)**2 + (GRID_SIZE_CONVERSION * yMove)**2,.5)
    targetAngle = angle_between(X_AXIS, (xMove, yMove))
    currRotation = LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"])

    turnAngle = targetAngle - currRotation

    turn(turnAngle)

    move(distance)

    return toPt