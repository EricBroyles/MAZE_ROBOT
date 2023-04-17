import time
from constants import *
from config import configRobot, orientToYAxis
from actions import *
from helpers import *
from nav import *

##CONFIG
configRobot()
orientToYAxis()

all_pos = [(0,0)]
all_sensors_data = []
ideal_dir_vec = (0, 1) #the y-axis
junc_items = []

try:
    found_exit = False

    while not(found_exit):

        #read sensors
        all_sensors_data.append(read()) #update sensors after any posible change to the orientation of the robot

        pos, real_dir_vec = getFinalPosAndVec(all_sensors_data, all_pos)
        all_pos.append(pos) #run this after any sensors are updated

        #begin moving forward
        startMove()

        #center the robot
        centered, turnMade = center(all_sensors_data[-1], all_sensors_data[-1]["any_gyroscope"], ideal_dir_vec) #posiblly changed the orientation of the robot
        
        if(turnMade):
            #update the sensors
            all_sensors_data.append(read()) #update sensors after any posible change to the orientation of the robot

            pos, real_dir_vec = getFinalPosAndVec(all_sensors_data, all_pos)
            all_pos.append(pos) #run this after any sensors are updated



        #check senario -> junction, dead end, exit, stop the robot if these senarios are encountered
        is_junc, is_deadend, is_exit, is_hallway = checkSenarios(all_sensors_data)

        if not(is_hallway):
            #create a junction when it is not the hallway
            createJunc(all_sensors_data, all_pos, ideal_dir_vec, junc_items) #adds the item to junc_items

        #if exit is found then break
        if is_exit:
            stop() #just in case
            break

        #if dead end -> run navigate back, quick thing to follow the back arrow to find a new junc with unexplored items

        #if at junction with no back arrows -> search juncs and find the closest one that has a non back arrow, if none error, generate a path to this


        #when to resume movement??????????????????????????????????????????????


        pass

    

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    print("You pressed ctrl+C...")
