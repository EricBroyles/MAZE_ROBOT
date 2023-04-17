from data import test_sensor_data
import math

def getFinalPosAndVec(all_sensors_data, all_prev_pos, wheel_dia = 1/math.pi):

    #error handling
    if(len(all_sensors_data) < 1):
        all_sensors_data.append(all_sensors_data[-1])
        
    elif(len(all_prev_pos) < 1):
        all_prev_pos = [(0,0)]

    if(not(-2 < -len(all_sensors_data))):
        prev_distance = ((all_sensors_data[-2]["left_motor"] + all_sensors_data[-2]["right_motor"]) / 2) / 360 * (math.pi * wheel_dia)
    else:
        prev_distance = 0

    distance = ((all_sensors_data[-1]["left_motor"] + all_sensors_data[-1]["right_motor"]) / 2) / 360 * (math.pi * wheel_dia)

    #convert this into a position with the angle
    x_dir_vec = math.cos(math.radians(all_sensors_data[-1]["any_gyroscope"]))
    y_dir_vec = math.sin(math.radians(all_sensors_data[-1]["any_gyroscope"]))
    
    x_pos, y_pos = (x_dir_vec * (distance - prev_distance), y_dir_vec * (distance - prev_distance))

    prev_x_pos, prev_y_pos = all_prev_pos[-1]
    final_pos = (x_pos + prev_x_pos, y_pos + prev_y_pos)
    
    final_dir_vec = (x_dir_vec, y_dir_vec)

    return final_pos, final_dir_vec

all_pos = [(0,0)]

# for i, item in enumerate(test_sensor_data):
#     #print(test_sensor_data[0:i+1])
#     pos, na = getFinalPosAndVec(test_sensor_data[0:i+1], all_pos)
#     print(pos)
#     all_pos.append(pos)
