import time
from constants import *
from config import configRobot
from actions import *
from helpers import *


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


try:
    found_exit = False
    while not(found_exit):
        pass

    

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    print("You pressed ctrl+C...")
