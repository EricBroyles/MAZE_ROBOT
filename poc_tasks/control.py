import time
from math import pi
from constants import *
from helpers import vectorRotation

def turn(delta):

    initDegree = LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"])
    print("@turn: initDegree = ", initDegree)

    target = initDegree + delta
    currDegree = initDegree

    #begin to turn

    #go cw -> right
    if(delta < 0):
        LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_LEFT"], TARGET_DPS)
        LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_RIGHT"], -TARGET_DPS)
        while(currDegree > target):
            time.sleep(DELAY / 2)
            currDegree = LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"])
            #print("currDegree ", currDegree)
        
    #go ccw -> left
    elif(delta > 0):
        LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_LEFT"], -TARGET_DPS)
        LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_RIGHT"], TARGET_DPS)
        while(currDegree < target):
            time.sleep(DELAY / 2)
            currDegree = LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"])
            #print("currDegree ", currDegree)
    else:
        print("@turn ERROR !!!!! no turn by 0 degree")
        return 0

    LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_LEFT"], 0)
    LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_RIGHT"], 0)
    print("@turn: done with ROTATION: ", LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"]), " vs currDegree: ", currDegree, "with initDegree: ", initDegree)



def move(distance):

    currLeftMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"])
    
    LEGO.offset_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"], currLeftMotorEncoder)
    currLeftMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"])
    finalEncoderVal = 360 * (abs(distance) / (pi * WHEEL_DIA_M))

    #either 1, or -1 for do a reverse

    #reversed logic due to orientation of the motors
    reverse = 1 if distance < 0 else -1

        

    LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_LEFT"], reverse * TARGET_DPS)
    LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_RIGHT"], reverse * TARGET_DPS)

    print(currLeftMotorEncoder, finalEncoderVal)

    while(abs(currLeftMotorEncoder) <= finalEncoderVal):
        time.sleep(DELAY)
        currLeftMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"])

    print("ENCODDERS SHOULD BE THE SAME -> LEFT: ", LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"]), " RIGHT: ", LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_RIGHT"]))
    
    LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_LEFT"], 0)
    LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_RIGHT"], 0)

def pause():
    LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_LEFT"], 0)
    LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_RIGHT"], 0)
    print("PAUSING")
    go = input("enter anything to start again: ")
    return go





def goToPoint(fromPt, toPt):
    fromPt = float(fromPt) + FLOATIFY
    fromPt = float(toPt) + FLOATIFY

    xMove = toPt[0] - fromPt[0]
    yMove = toPt[1] - fromPt[1]

    fromVec = Y_AXIS

    angleBetween = vectorRotation(fromVec, (xMove, 0))

    turn(angleBetween)
    print("moving by ", xMove)
    move(GRID_SIZE_CONVERSION * abs(xMove))

    angleBetween = vectorRotation((xMove, 0), (0, yMove))

    turn(angleBetween)
    move(GRID_SIZE_CONVERSION * abs(yMove))


    if (0, yMove/ abs(yMove)) != (0, 1):
        turn(-angleBetween * 2)

    return toPt


    # xMove = toPt[0] - fromPt[0]
    # yMove = toPt[1] - fromPt[1]

    # if fromPt == (0,0):
    #     fromPt = Y_AXIS

    # angleBetween = vectorRotation(fromPt, (xMove, 0))

    # turn(angleBetween)
    # move(xMove)

    # angleBetween = vectorRotation((xMove, 0), (0, yMove))

    # turn(angleBetween)
    # move(yMove)

    # if (0, yMove) != (0, 1):
    #     turn(-angleBetween * 2)






    # distance = pow((GRID_SIZE_CONVERSION * xMove)**2 + (GRID_SIZE_CONVERSION * yMove)**2,.5)

    # if toPt == (0,0):
    #     toVec = Y_AXIS
    # elif fromPt == (0,0):
    #     fromVec = Y_AXIS

    # angleBetween = vectorRotation(fromVec, toVec)
    # angleBetweenXAxis = vectorRotation(X_AXIS, toVec)

    # if angleBetween:
    #     turn(angleBetween + angleBetweenXAxis)

    # move(distance)

    # return fromVec
