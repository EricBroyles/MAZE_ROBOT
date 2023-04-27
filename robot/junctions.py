from helpers import *
from constants import *
from vectors import *

def addJuncItem(id, final_pos, is_expl, dir_vec, is_back, junc_items):
    junc_item = {"id": id, "is_expl": is_expl, "pos": final_pos, "dir_vec": dir_vec, "is_back": is_back}
    junc_items.append(junc_item)

def juncExist(junc_pos, junc_items, x_thresh = X_JUNC_THRESH, y_thresh = Y_JUNC_THRESH):

    """
    
    returns junc_exists and the id of the junc or None when no junc
    """
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

    """
    returns the id of the junc created, if not junc created then returns the id of the junction that already exists -> when the junc already exists
    """
    id = None
    is_expl = False

    #does the junction already exit, if so dont make the same junc again
    junc_exist, exist_id = juncExist(junc_pos, junc_items)
    if junc_exist:
        print("the junc exists so leaving")
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
                
                addJuncItem(id, junc_pos, is_expl, directions[loc], is_back, junc_items)

    #create the back junction
    is_back = True 
    #for the first two juncstion, the entrance and the first other the back arrow should be considered explored
    if id <= 2:
        #the back component for the second junction is already explored so as to not go back into the entrance
        is_expl = True
    addJuncItem(id, junc_pos, is_expl, directions["back"], is_back, junc_items)
    
    return id



# from helpers import *
# from constants import *
# from vectors import *

# def addJuncItem(id, connect_id, final_pos, is_expl, dir_vec, is_back, junc_items):
#     junc_item = {"id": id, "connect_id": connect_id, "is_expl": is_expl, "pos": final_pos, "dir_vec": dir_vec, "is_back": is_back}
#     junc_items.append(junc_item)
#     return junc_item

# def juncExist(prev_junc_id, junc_items):
#     """
#     @prev_junc_id: int -> the id of junc that the robot came from
#     @junc_items: [{junc_item}, ...]

#     Performs a look up to find if the junc that has been enetered already exists

#     returns the id of the junc that already exists, None if no junc exists
#     """
#     id = None

#     #try to find a junction that has "connect_id" == prev_junc_id



#     for junc in junc_items:
#         if junc["connect_id"] == prev_junc_id:
#             id = junc["id"]
#             break

#     return id

# def createConnections(prev_junc_id, new_back_junc_item, junc_items):
#     """
#     @prev_junc_id: int -> the id the robot was in before the current junc
#     @new_back_junc_item: {junc_item} -> a back arrow for the junction currently in
#     @junc_items: [{junc_item}, ...]

#     updates is_connect for at most two junc_items, the new_back_arrow and what it is connected to

#     """
#     curr_junc_id = new_back_junc_item["id"]
#     back_x, back_y = new_back_junc_item["dir_vec"]


#     for junc in (junc_items):
#         if junc["id"] == prev_junc_id and not junc["is_back"]:
#             x, y = junc["dir_vec"]
#             if -x == back_x and -y == back_y:
#                 #it is connected
#                 junc["connect_id"] = curr_junc_id
#                 break

#     for junc in junc_items:
#         if junc["id"] == curr_junc_id:
#             junc["connect_id"] = prev_junc_id
#             break

# # def __juncExist(junc_pos, junc_items, x_thresh = X_JUNC_THRESH, y_thresh = Y_JUNC_THRESH):

# #     """
# #     DEPRICATED -> reliant on positon data to perform a lookup to see if the junc already exits, position is inaccurate
# #     returns junc_exists and the id of the junc or None when no junc
# #     """
# #     x, y = junc_pos
# #     x_min, x_max = (x - x_thresh / 2, x + x_thresh / 2)
# #     y_min, y_max = (y - y_thresh / 2, y + y_thresh / 2)

# #     for item in junc_items:
# #         t_x, t_y = item['pos']
# #         if t_x >= x_min and t_x <= x_max:
# #             if t_y >= y_min and t_y <= y_max:
# #                 #the junction already exists
# #                 return True, item['id']
            
# #     #the junc does not already exist   
# #     return False, None


# #sensors_data = the most current reading
# #if junc_items has no items then we are adding the entrance
# ##assmues that the logic for a junction has been met!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# def createJunc(prev_junc_id, sensors_data, junc_pos, ideal_dir_vec, junc_items, space_ultra_thresh = SPACE_ULTRA_THRESH):

#     """

#     returns the id of the junc created, if not junc created then returns the id of the junction that already exists -> when the junc already exists
#     """
#     id = None
#     is_expl = False
#     connect_id = None

#     #does the junction already exit, if so dont make the same junc again
#     exist_id = juncExist(prev_junc_id, junc_items)
#     if exist_id is not None:
#         print("the junc exists so leaving")
#         return exist_id
    
#     #id is 1 for first item, and +1 to last id for any other
#     #note id is used to group multiple junctions, so multiple juncs share an id
#     if len(junc_items) == 0:
#         id = 1
#     else:
#         id = junc_items[-1]["id"] + 1

#     #find all other direction vectors for the given ideal_dir_vec
#     directions = getDirectionVectors(ideal_dir_vec) #{"front": (x,y), "right": ,  "left": , "back": }

#     #create the junction for any ultrasonic not seeing a wall
#     for key, val in sensors_data.items():
#         loc, type = getLocType(key, "string")
#         if type == "ultrasonic":
#             if val > space_ultra_thresh:
#                 is_back = False
                
#                 junc_item = addJuncItem(id, connect_id, junc_pos, is_expl, directions[loc], is_back, junc_items)

#     #create the back junction
#     is_back = True 
#     #for the first two juncstion, the entrance and the first other the back arrow should be considered explored
#     if id <= 2:
#         #the back component for the second junction is already explored so as to not go back into the entrance
#         is_expl = True
#     new_back_junc_item = addJuncItem(id, connect_id, junc_pos, is_expl, directions["back"], is_back, junc_items)
#     createConnections(prev_junc_id, new_back_junc_item, junc_items)

    
#     return id