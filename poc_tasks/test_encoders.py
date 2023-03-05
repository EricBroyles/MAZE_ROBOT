
import time
from config import configLEGO
from constants import *


configLEGO()




try:
    print("starting")
    baseTime = time.time()
    leftMotorDPS = TARGET_DPS
    rightMotorDPS = TARGET_DPS;
    currLeftMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"])
    currRightMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_RIGHT"])
    LEGO.offset_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"], currLeftMotorEncoder)
    LEGO.offset_motor_encoder(LEGO_ITEMS["MOTOR_RIGHT"], currRightMotorEncoder)

    

    LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_LEFT"], leftMotorDPS)
    LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_RIGHT"], rightMotorDPS)

    while True:
        print(LEGO.get_motor_status(LEGO_ITEMS["MOTOR_LEFT"]))
        print(LEGO.get_motor_status(LEGO_ITEMS["MOTOR_RIGHT"]))
        time.sleep(DELAY)

    while True:
        currTime = time.time()
        currLeftMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"])
        currRightMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_RIGHT"])
        print("time: ", (currTime - baseTime), "Right: ", rightMotorDPS, " vs Left: ", leftMotorDPS)
        
        actualRightMotorDPS = abs(currRightMotorEncoder) / ((currTime - baseTime))
        actualLeftMotorDPS = abs(currLeftMotorEncoder) / ((currTime - baseTime))

        print("ACTUALS STUFF time: ", (currTime - baseTime), "Right: ", actualRightMotorDPS, " vs Left: ", actualLeftMotorDPS)

        if actualRightMotorDPS != TARGET_DPS:
            if(actualRightMotorDPS < TARGET_DPS):
                rightMotorDPS += 10

            else:
                rightMotorDPS -= 10
            
            LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_RIGHT"], rightMotorDPS)

        if actualLeftMotorDPS != TARGET_DPS:
            if(actualLeftMotorDPS < TARGET_DPS):
                leftMotorDPS += 10

            else:
                leftMotorDPS -= 10

            LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_LEFT"], leftMotorDPS)
        time.sleep(DELAY / 2)
                

    
    print("done -> hit ctrl + c")

except KeyboardInterrupt:
    print("stopping")
    LEGO.reset_all()
