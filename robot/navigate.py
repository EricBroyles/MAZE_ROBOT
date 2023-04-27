
import math
from constants import *
from helpers import *
from vectors import *

def checkSenarios(curr_sensors, space_thresh = SPACE_ULTRA_THRESH, contact_thresh = CONTACT_ULTRA_THRESH, magnet_thresh = MAGNET_THRESH, ir_thresh = IR_THRESH, collision_thresh = COLLISION_THRESH):

    is_junc = False
    is_deadend = False #special type of junction
    is_exit = False #special type of junction
    is_hallway = False #not a junction
    is_hazard = False
    is_collision = False

    print("check the senario", curr_sensors['front_magnet'], getMag(curr_sensors['front_magnet']))

    is_hazard = True if getMag(curr_sensors['front_magnet']) >= magnet_thresh or curr_sensors['front_ir'] >= ir_thresh else False
    hazard_front = True if abs(curr_sensors['front_magnet']['y']) >= FRONT_MAGNET_THRESH or curr_sensors['front_ir'] >= ir_thresh else False
    print("hazard in front is ", hazard_front, curr_sensors['front_magnet']['y'])

    #get if front, left and right are seeing open space, True = seeing open space
    space_front = True if curr_sensors["front_ultrasonic"] > space_thresh else False
    space_right = True if curr_sensors["right_ultrasonic"] > space_thresh else False
    space_left  = True if curr_sensors["left_ultrasonic" ] > space_thresh else False

    contact_front = True if curr_sensors["front_ultrasonic"] <= contact_thresh or hazard_front else False
    wall_right = True if curr_sensors["right_ultrasonic"] <= space_thresh else False
    wall_left  = True if curr_sensors["left_ultrasonic" ] <= space_thresh else False

    is_collision = True if curr_sensors["left_ultrasonic"] <= collision_thresh or curr_sensors["right_ultrasonic"] <= collision_thresh else False

    

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

    return is_junc, is_deadend, is_exit, is_hallway, is_hazard, is_collision, hazard_front



def choosePath(ideal_dir_vec, junc_id, junc_items):

    """
    @junc_id == none give an arror
    when a path is choosen then is_expl is updated

    NOTE Updates the is_expl
    """


    if(junc_id is None):
        print("@choose path -> junc id is none")

    new_ideal_dir_vec = None #return none when there are no junctions available that have not been explored or back
    right_options = (None, None)
    left_options = (None, None)
    back_option = (None, None) #(index, {junction}) junction

    directions = getDirectionVectors(ideal_dir_vec)
    
    for i, item in enumerate(junc_items):
        if item['id'] == junc_id and not(item['is_expl']):

            if not(item['is_back']):
                if item['dir_vec'] == ideal_dir_vec:
                    new_ideal_dir_vec = item['dir_vec']
                    junc_items[i]['is_expl'] = True
                    return new_ideal_dir_vec
                elif item['dir_vec'] == directions['right']:
                    right_options = (i, item)
                    
                else:
                    left_options = (i, item)
                    
            else:
                back_option = i, item

    ir, right_junc = right_options
    il, left_junc = left_options
    ib, back_junc = back_option

    if right_junc is not None:
        junc_items[ir]['is_expl'] = True
        return right_junc['dir_vec']
    elif left_junc is not None:
        junc_items[il]['is_expl'] = True
        return left_junc['dir_vec']
    elif back_junc is not None:
        junc_items[ib]['is_expl'] = True
        return back_junc['dir_vec']

    return new_ideal_dir_vec


# def choosePath(ideal_dir_vec, junc_id, junc_items):

#     """
#     @junc_id == none give an arror
#     when a path is choosen then is_expl is updated
#     """


#     if(junc_id is None):
#         print("@choose path -> junc id is none")

#     new_ideal_dir_vec = None #return none when there are no junctions available that have not been explored or back
#     back_option = (None, None) #(index, {junction}) junction
    
#     for i, item in enumerate(junc_items):
#         if item['id'] == junc_id and not(item['is_expl']):

#             if not(item['is_back']):
#                 new_ideal_dir_vec = item['dir_vec']
#                 junc_items[i]['is_expl'] = True
#                 return new_ideal_dir_vec
#             else:
#                 back_option = i, item

#     i, back_junc = back_option
#     if back_junc is not None:
#         junc_items[i]['is_expl'] = True
#         return back_junc['dir_vec']

#     return new_ideal_dir_vec



