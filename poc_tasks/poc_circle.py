import time
from config import configLEGO
from constants import LEGO, LEGO_ITEMS, PWR, DELAY
from control import turn

print("Config Sensors Running")
configLEGO()

try:
    print("starting")
    #turn(-90)
    #turn(360)
    turn(-360)
    #while(True):
    #    print(LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"]))
    print("done -> hit ctrl + c")

except KeyboardInterrupt:
    print("stopping")
    LEGO.reset_all()


# import time
# import brickpi3 as BP
# import grovepi as GROVE

# LEGO = BP.BrickPi3()

# LEFT_MOTOR = BP.Port_A
# RIGHT_MOTOR = BP.Port_D
# GYRO_PORT = BP.Port_3

# DELAY = .02

# LEGO.set_sensor_type(GYRO_PORT, LEGO.SENSOR_TYPE.EV3_GYRO_ABS)
# print("config sensor")
# time.sleep(3)
# print("done config sensor -> test val: ", LEGO.get_sensor(GYRO_PORT))



# def turn(direction, degree, pwr = 40):

#     initRotation = LEGO.get_sensor(GYRO_PORT)[0]

#     if(direction == "RIGHT"):
#         #left goes forward
#         #right goes backward
#         LEGO.set_motor_power(LEFT_MOTOR, pwr)
#         LEGO.set_motor_power(RIGHT_MOTOR, -pwr)
#     else:
#         #left goes backward
#         #right goes forward
#         LEGO.set_motor_power(LEFT_MOTOR, -pwr)
#         LEGO.set_motor_power(RIGHT_MOTOR, pwr)
    
#     currRotation = LEGO.get_sensor(GYRO_PORT)[0]
#     delta = abs(degree)

#     print("\033[94m BEGIN @turn: currRotation =", currRotation, " vs initRotation = ", initRotation)
#     while(abs(currRotation) - abs(initRotation) < delta):
#         time.sleep(DELAY)
#         currRotation = LEGO.get_sensor(GYRO_PORT)[0]
#         print("\033[92m @turn: currRotation =", currRotation, " vs initRotation = ", initRotation)

#     print("\033[1m END @turn: currRotation =", currRotation, " vs initRotation = ", initRotation)  

#     LEGO.set_motor_power(LEFT_MOTOR, 0)
#     LEGO.set_motor_power(RIGHT_MOTOR, 0)

# try:
#     print("starting")
#     turn("RIGHT", 360)
#     print("done -> hit ctrl + c")

# except KeyboardInterrupt:
#     print("stopping")
#     LEGO.reset_all()
