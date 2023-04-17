from test_helpers import *
from getFinalPosAndVec import *

#assume no 3 way junctions, any 3 way is an exit
def checkSenarios(all_sensors_data, ultra_thresh = 30):

    is_junc = False
    is_deadend = False #special type of junction
    is_exit = False #special type of junction
    is_hallway = False #not a junction

    #get the current sensor reading
    curr_sensors = all_sensors_data[-1] #{of all sensors}

    #get if front, left and right are seeing open space, True = seeing open space
    front = True if curr_sensors["front_ultrasonic"] > ultra_thresh else False
    right = True if curr_sensors["right_ultrasonic"] > ultra_thresh else False
    left  = True if curr_sensors["left_ultrasonic" ] > ultra_thresh else False

    if front and right and left:
        #exit = all sensor are seeing open space
        is_exit = True

    elif not(front or right or left):
        #deadend = no sensor is seeing open space
        is_deadend = True
    
    elif front and not(right or left):
        #hallway = only when the front sensor is seeing open space
        is_hallway = True
    
    elif right or left:
        #junc = at lease the left or right sensor is seeing open space, could be more 
        is_junc = True

    if not(is_hallway):
        print("stop")
        #stop()

    return is_junc, is_deadend, is_exit, is_hallway

def addJuncItem(id, final_pos, is_expl, dir_vec, is_back, junc_items):
    junc_item = {"id": id, "is_expl": is_expl, "pos": final_pos, "dir_vec": dir_vec, "is_back": is_back}
    junc_items.append(junc_item)

##change these to X_JUNC_THRESH, Y_JUNC_THRESH
def juncExist(junc_pos, junc_items, x_thresh = .40, y_thresh = .40):

    x, y = junc_pos
    x_min, x_max = (x - x_thresh / 2, x + x_thresh / 2)
    y_min, y_max = (y - y_thresh / 2, y + y_thresh / 2)

    for item in junc_items:
        t_x, t_y = item['pos']
        if t_x >= x_min and t_x <= x_max:
            if t_y >= y_min and t_y <= y_max:
                #the junction already exists
                return True, item['id']
    #the junc does not already exist   
    return False, None


#sensors_data = the most current reading
#if junc_items has no items then we are adding the entrance
##assmues that the logic for a junction has been met!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def createJunc(sensors_data, junc_pos, ideal_dir_vec, junc_items, ultra_thresh = 30):
    id = None

    #does the junction already exit, if so dont make the same junc again
    junc_exist, exist_id = juncExist(junc_pos, junc_items)
    if junc_exist:
        return exist_id
    
    #id is 1 for first item, and +1 to last id for any other
    #note id is used to group multiple junctions, so multiple juncs share an id
    if len(junc_items) == 0:
        id = 1
    else:
        id = junc_items[-1]["id"] + 1
    
    #is_explored is only true if the item is the entrance, ie first item
    if id == 1:
        is_expl = True
    else:
        is_expl = False

    #find all other direction vectors for the given ideal_dir_vec
    directions = getDirectionVectors(ideal_dir_vec) #{"front": (x,y), "right": ,  "left": , "back": }

    #create the junction for any ultrasonic not seeing a wall
    for key, val in sensors_data.items():
        loc, type = getLocType(key, "string")
        if type == "ultrasonic":
            if val > ultra_thresh:
                is_back = False
                addJuncItem(id, junc_pos, is_expl, directions[loc], is_back, junc_items)

    #create the back junction
    is_back = True 
    if id == 2:
        #the back component for the second junction is already explored so as to not go back into the entrance
        is_expl = True
    addJuncItem(id, junc_pos, is_expl, directions["back"], is_back, junc_items)

    return id

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


# def createJunc(all_sensors_data, all_pos, ideal_dir_vec, junc_items, ultra_thresh = 30):

#     final_pos, not_used_real_dir_vec = getFinalPosAndVec(all_sensors_data, all_pos)
#     print(final_pos)
#     id = None

#     #id is 1 for first item, and +1 to last id for any other
#     #note id is used to group multiple junctions, so multiple juncs share an id
#     if len(junc_items) == 0:
#         id = 1
#     else:
#         id = junc_items[-1]["id"] + 1
    
#     #is_explored is only true if the item is the entrance, ie first item
#     if id == 1:
#         is_expl = True
#     else:
#         is_expl = False

#     #find all other direction vectors for the given ideal_dir_vec
#     directions = getDirectionVectors(ideal_dir_vec) #{"front": (x,y), "right": ,  "left": , "back": }

#     #create the junction for any ultrasonic not seeing a wall
#     for key, val in all_sensors_data[-1].items():
        
#         loc, type = getLocType(key, "string")
#         if type == "ultrasonic":
#             if val > ultra_thresh:
#                 is_back = False
#                 addJuncItem(id, final_pos, is_expl, directions[loc], is_back, junc_items)

#     #create the back junction
#     is_back = True 

#     #the back component for the second junction is already explored so as to not go back into the entrance
#     if id == 2:
#         is_expl = True

#     addJuncItem(id, final_pos, is_expl, directions["back"], is_back, junc_items)


    