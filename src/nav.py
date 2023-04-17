import math
from constants import *
from actions import *
from helpers import *
from inputs import *

def preventOverCenter(req_turn_angle, curr_raw_dir, ideal_dir_vec, center_thresh = CENTER_THRESH):
    x, y = ideal_dir_vec
    ideal_angle = math.atan2(y, x)

    #check if the requested turn angle combined with the robots current direction goes beyond the thresh from the ideal

    if req_turn_angle + curr_raw_dir - ideal_angle > center_thresh:
        turn_angle = center_thresh
    else:
        turn_angle = req_turn_angle

    return turn_angle

##NOTE As u center the front sensor will not be facing where it wants to be, nor will any of the sensors
##should only run this while moving in a hallway, does not work well with extereme values for ultra corresponding
# to junctions
#curr_raw_dir is the raw gyro reading, and dir_vec is the direction the robot should be facing 
#note sensor, should just be the current sensor reading in {} not [{}]
#this should never exceed 45 degrees or 40 degrees away from the center line
def center(sensor, curr_raw_dir, ideal_dir_vec):
    #centered
    centered = False
    turnMade = False

    # PID gains
    kp = 0.5
    ki = 0.1
    kd = 0.05

    # Setpoints
    setpoint = 10  # cm

    # Error variables
    error = sensor["left_ultrasonic"] - sensor["right_ultrasonic"]
    integral_error = 0
    derivative_error = 0
    prev_error = 0

    # Compute PID output
    integral_error += error
    derivative_error = error - prev_error
    output = kp*error + ki*integral_error + kd*derivative_error

    # Update previous error
    prev_error = error

    # Compute the turning angle based on the PID output and sensor values
    sensor_diff = abs(error)
    if sensor_diff <= 2:
        # Ultrasonics are close, use vectorTurn to turn back to ideal direction
        vecDeg = math.degrees(math.atan2(ideal_dir_vec[1], ideal_dir_vec[0]))
        if abs(curr_raw_dir - vecDeg) > 3:
            turn_angle = round(vecDeg - curr_raw_dir)
        else:
            turn_angle = 0

        centered = True
    elif sensor_diff <= setpoint:
        # Small difference, small turn angle
        turn_angle = round(output)
    else:
        # Large difference, large turn angle
        turn_angle = round(output + kp*sensor_diff)

    # Use the turn angle to adjust the robot's trajectory
    
    #the robot should never deviate more than CENTER_THRESH FROM THE ideal dir_vec
    turn_angle = preventOverCenter(turn_angle, curr_raw_dir, ideal_dir_vec)

    if(turn_angle != 0):
        turnMade = True
        turn(turn_angle)

    # return if the robot is centered
    return centered, turnMade

#assume no 3 way junctions, any 3 way is an exit
def checkSenarios(all_sensors_data, ultra_thresh = ULTRA_THRESH):

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
        stop()

    return is_junc, is_deadend, is_exit, is_hallway



def addJuncItem(id, final_pos, is_expl, dir_vec, is_back, junc_items):
    junc_item = {"id": id, "is_expl": is_expl, "pos": final_pos, "dir_vec": dir_vec, "is_back": is_back}
    junc_items.append(junc_item)


#raw_sensor_data = [{all items}]
#if junc_items has no items then we are adding the entrance
def createJunc(all_sensors_data, all_pos, ideal_dir_vec, junc_items, ultra_thresh = ULTRA_THRESH):

    final_pos, not_used_real_dir_vec = getFinalPosAndVec(all_sensors_data, all_pos)
    id = None

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
    for name, val  in all_sensors_data[-1].items():
        loc = getLoc(name)
        type = getType(name)

        if type == "ultrasonic":
            if val > ultra_thresh:
                is_back = False
                addJuncItem(id, final_pos, is_expl, directions[loc], is_back, junc_items)

    #create the back junction
    is_back = True 

    #the back component for the second junction is already explored so as to not go back into the entrance
    if id == 2:
        is_expl = True

    addJuncItem(id, final_pos, is_expl, directions["back"], is_back, junc_items)
    



# #exits if it finds the exit,ie all 3 sensors are reading large values
# #exits when it hits a dead end, all 3 sensors reading a small val
# #documents path_items and junc_items as it goes

# #assumes that it is orientated to go forward
# #init_dir_vec is the vector the robot is facing at the time explore begins
# def explore(path_items, junc_items, all_raw_pos, all_pos, init_dir_vec):
#     found_exit = False
#     found_deadend = False

#     all_sens = read() #dic of items
#     dir_vec = init_dir_vec
    

#     while not(found_exit or found_deadend):
#         startMove()

#         center(all_sens, all_sens["any_gyroscope"], dir_vec) #this will cause variation in the encoders!!!!!!

#         front = all_sens["front_ultrasonic"]
#         left = all_sens["left_ultrasonic"]
#         right = all_sens["right_ultrasonic"]

#         if(front > ULTRA_THRESH and left > ULTRA_THRESH and right > ULTRA_THRESH):
#             stop()
#             print("reached an exit")
#             found_exit = True
            

#         elif(front < ULTRA_THRESH and left < ULTRA_THRESH and right < ULTRA_THRESH):
#             stop()
#             print("reached dead end")
#             found_deadend = True
            
        
#         elif(right > ULTRA_THRESH or left > ULTRA_THRESH):
#             stop()
            
#             #create a path item
#             #create a junction item


        
#         else:
#             #continue forward


#         #add the junction
#         #add the path


        



#         #update all sensors
#         #update dir vec

#     #start going forward, 

#     #run center logic

#     #puasue when a junction is detected, to create the path_item and junc_item
#     #if any created junc are uncertain then continue moving forward until 
#     #   either the left or right sensor will go away, but the front still sees space so then the uncertain junc is correct
#     #   or the left or irght will cont detecting space and the front will see a wall, so then then remove the uncertain junc, and use the pos u are at now



#     #pause when cant go forward no more and exit
#     #pause when all sensors are seeing open space and exit with TRUE

#     #if created jucntion exits, go down the one that matches the current vector of travel
#     #otherwise go down any of the other junc









#     return found_exit