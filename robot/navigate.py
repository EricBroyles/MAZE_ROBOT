
import math
from constants import *
from helpers import *
from vectors import *

def checkSenarios(curr_sensors, space_thresh = SPACE_ULTRA_THRESH, contact_thresh = CONTACT_ULTRA_THRESH):

    is_junc = False
    is_deadend = False #special type of junction
    is_exit = False #special type of junction
    is_hallway = False #not a junction

    #get if front, left and right are seeing open space, True = seeing open space
    space_front = True if curr_sensors["front_ultrasonic"] > space_thresh else False
    space_right = True if curr_sensors["right_ultrasonic"] > space_thresh else False
    space_left  = True if curr_sensors["left_ultrasonic" ] > space_thresh else False

    contact_front = True if curr_sensors["front_ultrasonic"] <= contact_thresh else False
    wall_right = True if curr_sensors["right_ultrasonic"] <= space_thresh else False
    wall_left  = True if curr_sensors["left_ultrasonic" ] <= space_thresh else False

    if space_front and space_right and space_left:
        #exit = all sensor are seeing open space
        is_exit = True

    elif contact_front and wall_right and wall_left:
        #deadend = no sensor is seeing open space
        is_deadend = True
    
    # elif space_front and wall_right and wall_left:
    #     #hallway = only when the front sensor is seeing open space
    #     is_hallway = True
    
    elif space_right or space_left:
        #junc = at lease the left or right sensor is seeing open space, could be more 
        is_junc = True

    if not(is_exit or is_deadend or is_junc):
        is_hallway = True

    return is_junc, is_deadend, is_exit, is_hallway

#assumes the motor encoders only increase in position
def getFinalPosAndVec(all_sensors_data, all_prev_pos, wheel_dia = WHEEL_DIA):

    #error handling
    if(len(all_sensors_data) < 1):
        all_sensors_data.append(all_sensors_data[-1])
        
    elif(len(all_prev_pos) < 1):
        all_prev_pos = [(0,0)]

    if(not(-2 < -len(all_sensors_data))):
        prev_distance = abs((all_sensors_data[-2]["left_motor"] + all_sensors_data[-2]["right_motor"]) / 2) / 360 * (math.pi * wheel_dia)
    else:
        prev_distance = 0

    distance = abs((all_sensors_data[-1]["left_motor"] + all_sensors_data[-1]["right_motor"]) / 2) / 360 * (math.pi * wheel_dia)

    #convert this into a position with the angle
    x_dir_vec = math.cos(math.radians(all_sensors_data[-1]["any_gyroscope"]))
    y_dir_vec = math.sin(math.radians(all_sensors_data[-1]["any_gyroscope"]))
    
    x_pos, y_pos = (x_dir_vec * (distance - prev_distance), y_dir_vec * (distance - prev_distance))

    prev_x_pos, prev_y_pos = all_prev_pos[-1]
    final_pos = (x_pos + prev_x_pos, y_pos + prev_y_pos)
    
    final_dir_vec = (x_dir_vec, y_dir_vec)

    return final_pos, final_dir_vec


def choosePath(junc_id, junc_items):

    new_ideal_dir_vec = None #return none when there are no junctions available that have not been explored or back
    back_option = (None, None) #(index, {junction}) junction
    
    for i, item in enumerate(junc_items):
        if item['id'] == junc_id and not(item['is_expl']):

            if not(item['is_back']):
                new_ideal_dir_vec = item['dir_vec']
                junc_items[i]['is_expl'] = True
                return new_ideal_dir_vec
            else:
                back_option = i, item

    i, back_junc = back_option
    if back_junc is not None:
        junc_items[i]['is_expl'] = True
        return back_junc['dir_vec']

    return new_ideal_dir_vec



