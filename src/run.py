import time
from constants import *
from config import configRobot, orientToYAxis
from actions import *
from helpers import *
from nav import *


def addJuncItem(id, final_pos, is_expl, dir_vec, is_back, junc_items):
    junc_item = {"id": id, "is_expl": is_expl, "pos": final_pos, "dir_vec": dir_vec, "is_back": is_back}
    junc_items.append(junc_item)


#raw_sensor_data = [{all items}]
#if junc_items has no items then we are adding the entrance
def createJunc(curr_dir_vec, raw_sensor_data, junc_items):
    final_pos, dir_vec = getFinalPosAndVec(raw_sensor_data)
    id = None
    if len(junc_items) == 0:
        id = 1
    else:
        id = junc_items[-1]["id"] + 1
    
    if id == 1:
        is_expl = True
    else:
        is_expl = False

    curr_sensor = raw_sensor_data[-1]
    directions = getDirectionVectors(curr_dir_vec)

    #create the junction for any ultrasonic not seeing a wall
    for name, val  in curr_sensor.items():
        loc = getLoc(name)
        type = getType(name)

        
        if type == "ultrasonic":
            if val > ULTRA_THRESH:
                addJuncItem(id, final_pos, is_expl, dir_vec[loc], False, junc_items)

    #create the back junction 
    #the back component for the second junction is already explored so as to not go back into the entrance
    if id == 2:
        is_expl = True
    addJuncItem(id, final_pos, is_expl, dir_vec["back"], True, junc_items)



##CONFIG
configRobot()
orientToYAxis()

all_pos = [(0,0)]
all_sensors_data = []
ideal_dir_vec = (0, 1) #the y-axis

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

        #if junction create a junction

        #if exit is found then break

        #if dead end -> run navigate back, quick thing to follow the back arrow to find a new junc with unexplored items

        #if at junction with no back arrows -> search juncs and find the closest one that has a non back arrow, if none error, generate a path to this


        #when to resume movement??????????????????????????????????????????????
        #when are the encoders being reset to understand the position?????????????????????


        pass

    

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    print("You pressed ctrl+C...")
