import math
from actions import *
from vectors import *


def findTurnAngle(sensors, ideal_dir_vec):
    centered = False
    turn_angle = 0

    curr_raw_dir = sensors["any_gyroscope"]

    curr_raw_dir_vec = angleToVector(curr_raw_dir)
    curr_angle_cure = vectorRotation(ideal_dir_vec, curr_raw_dir_vec) #how much angle is already being applied to center the robot

    # PID gains
    kp = 0.5
    ki = 0.1
    kd = 0.1

    # Error variables
    error =  sensors["left_ultrasonic"] - sensors["right_ultrasonic"]

    output = kp*error + ki*error + kd*error

    output -= curr_angle_cure

    if(output > 40):
        output = 40
    elif(output < -40):
        output = -40

    turn_angle = output
    
    #when the ultrasonics aree close to another, set back to face the ideal
    if(abs(error) < 10):
        turn_angle = -curr_angle_cure
        centered = True

    return turn_angle, centered

#38 is output for 40cm
# print(findTurnAngle({"left_ultrasonic": 20,"right_ultrasonic": 20, "any_gyroscope": 110}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 20, "any_gyroscope": 110}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 20, "any_gyroscope": 90}, (0,1)))

# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 30, "any_gyroscope": 110}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 30, "any_gyroscope": 90}, (0,1)))

# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 500, "any_gyroscope": 110}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 500, "any_gyroscope": 90}, (0,1)))


# print()
# print(findTurnAngle({"left_ultrasonic": 20,"right_ultrasonic": 20, "any_gyroscope": 70}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 20, "any_gyroscope": 70}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 20, "any_gyroscope": 90}, (0,1)))

# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 30, "any_gyroscope": 70}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 30, "any_gyroscope": 90}, (0,1)))

# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 500, "any_gyroscope": 70}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 500, "any_gyroscope": 90}, (0,1)))


##NOTE As u center the front sensor will not be facing where it wants to be, nor will any of the sensors
##should only run this while moving in a hallway, does not work well with extereme values for ultra corresponding
# to junctions
#curr_raw_dir is the raw gyro reading, and dir_vec is the direction the robot should be facing 
#note sensor, should just be the current sensor reading in {} not [{}]
#this should never exceed 45 degrees or 40 degrees away from the center line

##WILL NOT WORK IN A JUNCTION or TURN, will over correct
def center(sensors, ideal_dir_vec):

    turn_made = False
    
    turn_angle, centered = findTurnAngle(sensors, ideal_dir_vec)

    print("@center: ", turn_angle)
    if(turn_angle != 0):
        turn_made = True
        turn(turn_angle, "no_stop")
  
    # return if the robot is centered
    return centered, turn_made
