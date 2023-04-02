import time
from constants import *
from config import configRobot
from actions import *
from helpers import *
from inputs import read



  



##CONFIG
configRobot()


try:
    
    found_exit = False
    #while True:
    #    print("read: ", read("gyroscope"))
    #    #print("read: ", read("ultrasonic"))
    move(.305)
    move(-.305)
    turn(90)
    turn(-90)
    #turn(360)
    #turn(-360)
    startMove()
    print("has flow moved")
    time.sleep(5)
    stop()

    

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    stop()
    print("You pressed ctrl+C...")
