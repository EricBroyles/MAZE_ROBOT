from inputs import *
from navigate import *

##Perform the updates to the sensors of the robot and the positon of the robot
#should run after a ======= start stop seq
#start stop seq: (after any call to stop, move(distance), centerInJunc)
def updateAfterStartStop(all_sensors_data, all_raw_pos, all_pos, do_norm_encoders = True):
    reading = read()

    #update the sensors
    all_sensors_data.append(reading)

    all_raw_pos.append(reading)

    #update the position data
    real_dir_vec = updatePos(all_raw_pos, all_pos, do_norm_encoders)
    
    return real_dir_vec

def updatePos(all_raw_pos, all_prev_pos, do_norm_encoders = False, wheel_dia = WHEEL_DIA):
    """
    NOTE this should be called after any start and stop sequence that moves the robot

    @all_raw_pos: list of {each sensor at some time}
    @all_prev_pos: list of (x, y) -> all previous calculated final pos of the robot
    @do_norm_encoder: T/F -> should the wheel_dia that reduces encoder error be calculated (F -> use the passed wheel_dia)

    NOTE updates the all_prev_pos array directly

    returns the true vector that the robot is facing
    """
    
    #error handling when lists are too short
    if(len(all_raw_pos) <= 1):
        print("ERROR @updatePos -> all_raw_pos is too short: ", all_raw_pos)
        return 0 
    if(len(all_prev_pos) == 0):
        all_prev_pos = [(0,0)]

    #finding the difference in encoder from last sensor reading vs second to last reading
    prev_encoder_ticks = abs((all_raw_pos[-2]["left_motor"] + all_raw_pos[-2]["right_motor"]) / 2)
    curr_encoder_ticks = abs((all_raw_pos[-1]["left_motor"] + all_raw_pos[-1]["right_motor"]) / 2)
    new_encoder_ticks = curr_encoder_ticks - prev_encoder_ticks

    #if do_norm_encoders then find the wheel_dia to reduce error of encoders
    if do_norm_encoders:
        wheel_dia = normEncodersFunc(new_encoder_ticks)

    #find the distance traveled
    new_distance = new_encoder_ticks / 360 * (math.pi * wheel_dia)

    #find the real_dir_vec the robot is facing
    x_dir_vec = math.cos(math.radians(all_raw_pos[-1]["any_gyroscope"]))
    y_dir_vec = math.sin(math.radians(all_raw_pos[-1]["any_gyroscope"]))
    final_dir_vec = (x_dir_vec, y_dir_vec)

    #find the amount moved in the x, and y and the prev pos the robot was at
    new_x_move, new_y_move = (x_dir_vec * new_distance, y_dir_vec * new_distance)
    prev_x_pos, prev_y_pos = all_prev_pos[-1]

    #update the all_position with the new movement
    final_pos = (new_x_move + prev_x_pos, new_y_move + prev_y_pos)
    all_prev_pos.append(final_pos)

    print("\n-----------------------------------------------------------")
    print("UPDATED POS")
    print("\nfinal_pos: ", final_pos)
    print("-----------------------------------------------------------\n")

    return final_dir_vec

def updateHazards(curr_sensors, curr_pos, hazards, hazard_params, magnet_thresh = MAGNET_THRESH, ir_thresh = IR_THRESH):
    name = None
    reading = None
    if getMag(curr_sensors['front_magnet']) >= magnet_thresh or abs(curr_sensors['front_magnet']['y']):

        name = "magnet"
        reading = getMag(curr_sensors['front_magnet'])
    elif curr_sensors['front_ir'] >= ir_thresh:
        name = "heat"
        reading = curr_sensors['front_ir']
    else:
        return
    
    x, y = curr_pos
    id = len(hazards) + 1
    # haz_already_exist = False

    # for n, pos in hazards.items():
    #     x_t, y_t = pos

    #     if abs(x - x_t) < .40 and abs(y-y_t) < .40 and (n[:4] == name[:4]):
    #         haz_already_exist = True
    #         break

    # if not haz_already_exist:
    if name is not None and reading is not None:
        hazards[name + str(id)] = curr_pos
        hazard_params[name + str(id)] = reading



# #assumes the motor encoders only increase in position
# #assumes that each item in all_sensors_data represents a start stop sequence of the motor
# def getFinalPosAndVec(all_sensors_data, all_prev_pos, do_norm_encoders = False, wheel_dia = WHEEL_DIA):

#     prev_encoder_ticks = abs((all_sensors_data[-2]["left_motor"] + all_sensors_data[-2]["right_motor"]) / 2)
#     curr_encoder_ticks = abs((all_sensors_data[-1]["left_motor"] + all_sensors_data[-1]["right_motor"]) / 2)

#     if do_norm_encoders:
#         encoder_ticks = curr_encoder_ticks - prev_encoder_ticks
#         wheel_dia = normEncodersFunc(encoder_ticks)

#     #error handling
#     if(len(all_sensors_data) < 1):
#         all_sensors_data.append(all_sensors_data[-1])
        
#     elif(len(all_prev_pos) < 1):
#         all_prev_pos = [(0,0)]

#     if(not(-2 < -len(all_sensors_data))):
#         prev_distance = prev_encoder_ticks / 360 * (math.pi * wheel_dia)
#     else:
#         prev_distance = 0

#     distance = curr_encoder_ticks / 360 * (math.pi * wheel_dia)

#     #convert this into a position with the angle
#     x_dir_vec = math.cos(math.radians(all_sensors_data[-1]["any_gyroscope"]))
#     y_dir_vec = math.sin(math.radians(all_sensors_data[-1]["any_gyroscope"]))
    
#     x_pos, y_pos = (x_dir_vec * (distance - prev_distance), y_dir_vec * (distance - prev_distance))

#     prev_x_pos, prev_y_pos = all_prev_pos[-1]
#     final_pos = (x_pos + prev_x_pos, y_pos + prev_y_pos)
    
#     final_dir_vec = (x_dir_vec, y_dir_vec)

#     return final_pos, final_dir_vec