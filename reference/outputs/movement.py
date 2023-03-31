import time
from main import myRobot
from math import pi
from constants import *


def turn(delta):

    initDegree = myRobot.readData("gyroscope")
    print("@turn: initDegree = ", initDegree)

    target = initDegree + delta
    currDegree = initDegree

    #begin to turn

    #go cw -> right
    if(delta < 0):
        myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_LEFT"], TARGET_DPS)
        myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_RIGHT"], -TARGET_DPS)
        while(currDegree > target):
            time.sleep(DELAY / 2)
            currDegree = myRobot.lego.get_sensor(myRobot.lego_ITEMS["EV3_GYRO"])
            #print("currDegree ", currDegree)
        
    #go ccw -> left
    elif(delta > 0):
        myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_LEFT"], -TARGET_DPS)
        myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_RIGHT"], TARGET_DPS)
        while(currDegree < target):
            time.sleep(DELAY / 2)
            currDegree = myRobot.lego.get_sensor(myRobot.lego_ITEMS["EV3_GYRO"])
            #print("currDegree ", currDegree)
    else:
        print("@turn ERROR !!!!! no turn by 0 degree")
        return 0

    myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_LEFT"], 0)
    myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_RIGHT"], 0)
    print("@turn: done with ROTATION: ", myRobot.lego.get_sensor(myRobot.lego_ITEMS["EV3_GYRO"]), " vs currDegree: ", currDegree, "with initDegree: ", initDegree)



def move(distance):

    currLeftMotorEncoder = myRobot.lego.get_motor_encoder(myRobot.lego_ITEMS["MOTOR_LEFT"])
    
    myRobot.lego.offset_motor_encoder(myRobot.lego_ITEMS["MOTOR_LEFT"], currLeftMotorEncoder)
    currLeftMotorEncoder = myRobot.lego.get_motor_encoder(myRobot.lego_ITEMS["MOTOR_LEFT"])
    finalEncoderVal = 360 * (abs(distance) / (pi * WHEEL_DIA_M))

    #either 1, or -1 for do a reverse

    #reversed logic due to orientation of the motors
    reverse = 1 if distance < 0 else -1

        

    myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_LEFT"], reverse * TARGET_DPS)
    myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_RIGHT"], reverse * TARGET_DPS)

    print(currLeftMotorEncoder, finalEncoderVal)

    while(abs(currLeftMotorEncoder) <= finalEncoderVal):
        time.sleep(DELAY)
        currLeftMotorEncoder = myRobot.lego.get_motor_encoder(myRobot.lego_ITEMS["MOTOR_LEFT"])

    print("ENCODDERS SHOULD BE THE SAME -> LEFT: ", myRobot.lego.get_motor_encoder(myRobot.lego_ITEMS["MOTOR_LEFT"]), " RIGHT: ", myRobot.lego.get_motor_encoder(myRobot.lego_ITEMS["MOTOR_RIGHT"]))
    
    myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_LEFT"], 0)
    myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_RIGHT"], 0)

def pause():
    myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_LEFT"], 0)
    myRobot.lego.set_motor_dps(myRobot.lego_ITEMS["MOTOR_RIGHT"], 0)
    print("PAUSING")
    go = input("enter anything to start again: ")
    return go
