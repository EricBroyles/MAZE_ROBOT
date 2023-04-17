from helpers import *
from constants import *
from vectors import *

def addJuncItem(id, final_pos, is_expl, dir_vec, is_back, junc_items):
    junc_item = {"id": id, "is_expl": is_expl, "pos": final_pos, "dir_vec": dir_vec, "is_back": is_back}
    junc_items.append(junc_item)

##change these to X_JUNC_THRESH, Y_JUNC_THRESH
def juncExist(junc_pos, junc_items, x_thresh = X_JUNC_THRESH, y_thresh = Y_JUNC_THRESH):

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

def createJunc(sensors_data, junc_pos, ideal_dir_vec, junc_items, space_ultra_thresh = SPACE_ULTRA_THRESH):
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

    #find all other direction vectors for the given ideal_dir_vec
    directions = getDirectionVectors(ideal_dir_vec) #{"front": (x,y), "right": ,  "left": , "back": }

    #create the junction for any ultrasonic not seeing a wall
    for key, val in sensors_data.items():
        loc, type = getLocType(key, "string")
        if type == "ultrasonic":
            if val > space_ultra_thresh:
                is_back = False
                is_expl = False
                addJuncItem(id, junc_pos, is_expl, directions[loc], is_back, junc_items)

    #create the back junction
    is_back = True 
    #for the first two juncstion, the entrance and the first other the back arrow should be considered explored
    if id <= 2:
        #the back component for the second junction is already explored so as to not go back into the entrance
        is_expl = True
    addJuncItem(id, junc_pos, is_expl, directions["back"], is_back, junc_items)

    return id, junc_exist