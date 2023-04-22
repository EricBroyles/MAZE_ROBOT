

import time     # import the time library for the sleep function
from lib import brickpi3 # import the BrickPi3 drivers
from lib import grovepi
from lib.MPU9250 import MPU9250
import math

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

try:
    mpu9250 = MPU9250()
    sensor1= 1 # Pin 14 is A0 Port.
    grovepi.pinMode(sensor1,"INPUT")
   
except IOError as error:
    print(error)

try:
    while True:
        try:
            magThreshold = 100
            mag = mpu9250.readMagnet()
            mag_x = mag['x']
            mag_y = mag['y']
            mag_z = mag['z']
            magMagnitude = math.sqrt(mag_x**2 + mag_y**2 + mag_z**2)
            print("Magnetic: ",magMagnitude)
           
            if(magMagnitude > magThreshold):
                print("Magnet Detected")
           
            irThreshold = 100
            sensor1_value = grovepi.analogRead(sensor1)
            irMagnitude = sensor1_value
            print("IR: ",irMagnitude)
            if(irMagnitude > irThreshold):
                print("IR Detected")
           
            time.sleep(.1)

        except IOError as error:
            print(error)
            time.sleep(0.5)  
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
