import time
from math import pi
from constants import *
from helpers import vectorRotation

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
    
    LEGO.offset_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"], currLeftMotorEncoder)
    currLeftMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"])
    finalEncoderVal = 360 * (abs(distance) / (pi * WHEEL_DIA_M))

    #either 1, or -1 for do a reverse
    reverse = -1 if distance < 0 else 1

        

    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], reverse * PWR)
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], reverse * PWR)

    print(currLeftMotorEncoder, finalEncoderVal)

    while(abs(currLeftMotorEncoder) <= finalEncoderVal):
        time.sleep(DELAY)
        currLeftMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"])

    print("ENCODDERS SHOULD BE THE SAME -> LEFT: ", LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"]), " RIGHT: ", LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_RIGHT"]))
    
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], 0)
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], 0)

def pause():
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], 0)
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], 0)
    print("PAUSING")
    go = input("enter anything to start again: ")
    return go

def goToPoint(fromVec, toVec):

    angleBetween = vectorRotation(fromVec, toVec)

    xMove = toVec[0] - fromVec[0]
    yMove = toVec[1] - fromVec[1]

    distance = pow((GRID_SIZE_CONVERSION * xMove)**2 + (GRID_SIZE_CONVERSION * yMove)**2,.5)

    if angleBetween:
        turn(angleBetween)

    move(distance)

    return fromVec
