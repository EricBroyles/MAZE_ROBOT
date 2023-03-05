# it's a text file :D
"""
Senses whether there is a wall obstructing the robot or not
using ultrasonic.
If a wall is detected, it will check other sensors for
open space. If there is no wall option available, it will 
turn 180 degrees. 

Only turns orientation toward open space. Does not move forward.
"""

import grovepi
import control
from constants import *
from config import configLEGO

configLEGO()

WALL_HERE = 50

ultrasonic_front = 2
ultrasonic_right = 7
ultrasonic_left = 4

try:

    #LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_LEFT"], TARGET_DPS)
    #LEGO.set_motor_dps(LEGO_ITEMS["MOTOR_RIGHT"], TARGET_DPS)

    while True:

        front = grovepi.ultrasonicRead(ultrasonic_front)
        left = grovepi.ultrasonicRead(ultrasonic_left)
        right = grovepi.ultrasonicRead(ultrasonic_right)
        print("front: ", front, " left: ", left, " right: ", right)
        time.sleep(DELAY / 2)
    
    while False:

        if grovepi.ultrasonicRead(ultrasonic_front) < WALL_HERE: # wall in front
            LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], 0)
            LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], 0)
            print("WALL - Front Sensor")

        if grovepi.ultrasonicRead(ultrasonic_left) > WALL_HERE: # no wall left
            control.turn(1) # positive delta = turn left
            print("Left sensor clear. Turn left.")

        elif grovepi.ultrasonicRead(ultrasonic_right) > WALL_HERE: # no wall right
            control.turn(-1) # negative delta = turn right
            print("Right sensor clear. Turn right.")

        else: # walls everywhere ahhh
            for x in range(2): # turns 90 degrees twice
                control.turn(1) 
            print("No directions clear. Turn around.")

        time.sleep(DELAY / 2)

except KeyboardInterrupt:
    print("You pressed ctrl+C...")
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], 0)
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], 0)
