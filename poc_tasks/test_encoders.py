
from config import configLEGO
from constants import *

configLEGO()


try:
    print("starting")
    currLeftMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"])
    currRightMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_RIGHT"])
    LEGO.offset_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"], currLeftMotorEncoder)
    LEGO.offset_motor_encoder(LEGO_ITEMS["MOTOR_RIGHT"], currRightMotorEncoder)

    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], PWR)
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], PWR)
    while True:
        currLeftMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_LEFT"])
        currRightMotorEncoder = LEGO.get_motor_encoder(LEGO_ITEMS["MOTOR_RIGHT"])
        print("Right: ", currRightMotorEncoder, " vs Left: ", currLeftMotorEncoder)
    
    print("done -> hit ctrl + c")

except KeyboardInterrupt:
    print("stopping")
    LEGO.reset_all()
