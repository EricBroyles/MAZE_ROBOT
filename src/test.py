# def checkSenarios(raw_sensor_data):
import math

#raw_sensor: {all sensor readings or just the encoders and gyro} -> must have at lease one item
#all_prev_pos: [(x, y), ....] -> must have at least one item
def getFinalPosAndVec(raw_sensor_data, all_prev_pos, wheel_dia = 1/math.pi):

    if(len(raw_sensor_data) < 1):
        print("ERROR at getFINALPOSANDVEC raw_sensor_data is too short")
        return
    elif(len(all_prev_pos) < 1):
        all_prev_pos = [(0,0)]

    if(not(-2 < -len(raw_sensor_data))):
        prev_distance = ((raw_sensor_data[-2]["left_motor"] + raw_sensor_data[-2]["right_motor"]) / 2) / 360 * (math.pi * wheel_dia)
    else:
        prev_distance = 0

    distance = ((raw_sensor_data[-1]["left_motor"] + raw_sensor_data[-1]["right_motor"]) / 2) / 360 * (math.pi * wheel_dia)

    #convert this into a position with the angle
    x_dir_vec = math.cos(math.radians(raw_sensor_data[-1]["any_gyroscope"]))
    y_dir_vec = math.sin(math.radians(raw_sensor_data[-1]["any_gyroscope"]))
    
    x_pos, y_pos = (x_dir_vec * (distance - prev_distance), y_dir_vec * (distance - prev_distance))

    prev_x_pos, prev_y_pos = all_prev_pos[-1]
    final_pos = (x_pos + prev_x_pos, y_pos + prev_y_pos)
    
    final_dir_vec = (x_dir_vec, y_dir_vec)

    return final_pos, final_dir_vec

print("testing")

test = [{"left_motor": 0, "right_motor": 0, "any_gyroscope": 90}, {"left_motor": 360, "right_motor": 360, "any_gyroscope": 90}, {"left_motor": 720, "right_motor": 720, "any_gyroscope": 0}, {"left_motor": 1080, "right_motor": 1080, "any_gyroscope": -90}, {"left_motor": 1440, "right_motor": 1440, "any_gyroscope": -180}]
pos = [(0,0)]
for i, item in enumerate(test):
    p, v = getFinalPosAndVec(test[0:i+1], pos)
    print(p, v)
    pos.append(p)


# test_sensors = [test[0]]
# test_pos = [(0,0)]
# for i in range(0, len(test)+1):
#     a, na = getFinalPosAndVec(test_sensors, test_pos)
#     test_sensors.append(testitem)
#     test_pos.append(a)
#     print(item, a, na)


#  import math

# def getFinalPosAndVec(raw_sensor_data, wheel_dia = 1/math.pi):
    
#     final_pos = (0, 0)
#     final_dir_vec = (1, 0) #corresponds to 0 degrees
#     prev_distance = 0

#     for item in raw_sensor_data:
#         distance = ((item["left_motor"] + item["right_motor"]) / 2) / 360 * (math.pi * wheel_dia)

#         #convert this into a position with the angle
#         x_dir_vec = math.cos(math.radians(item["any_gyroscope"]))
#         y_dir_vec = math.sin(math.radians(item["any_gyroscope"]))
#         x_pos, y_pos = (x_dir_vec * (distance - prev_distance), y_dir_vec * (distance - prev_distance))
#         prev_x_pos, prev_y_pos = final_pos

#         final_pos = (x_pos + prev_x_pos, y_pos + prev_y_pos)
        
#         final_dir_vec = (x_dir_vec, y_dir_vec)

#         prev_distance = distance

#     return final_pos, final_dir_vec

# print("testing")
# print(getFinalPosAndVec([{"left_motor": 0, "right_motor": 0, "any_gyroscope": 90}]))
# print(getFinalPosAndVec([{"left_motor": 0, "right_motor": 0, "any_gyroscope": 90}, {"left_motor": 360, "right_motor": 360, "any_gyroscope": 90}]))
# print(getFinalPosAndVec([{"left_motor": 0, "right_motor": 0, "any_gyroscope": 90}, {"left_motor": 360, "right_motor": 360, "any_gyroscope": 90}, {"left_motor": 720, "right_motor": 720, "any_gyroscope": 0}]))
# print(getFinalPosAndVec([{"left_motor": 0, "right_motor": 0, "any_gyroscope": 90}, {"left_motor": 360, "right_motor": 360, "any_gyroscope": 90}, {"left_motor": 720, "right_motor": 720, "any_gyroscope": 0}, {"left_motor": 1080, "right_motor": 1080, "any_gyroscope": -90}]))
# print(getFinalPosAndVec([{"left_motor": 0, "right_motor": 0, "any_gyroscope": 90}, {"left_motor": 360, "right_motor": 360, "any_gyroscope": 90}, {"left_motor": 720, "right_motor": 720, "any_gyroscope": 0}, {"left_motor": 1080, "right_motor": 1080, "any_gyroscope": -90}, {"left_motor": 1440, "right_motor": 1440, "any_gyroscope": -180}]))

# def getRightLeftVectors(front_vector):
#     # Ensure that the input vector has unit length
#     magnitude = (front_vector[0]**2 + front_vector[1]**2)**0.5
#     front_vector = (front_vector[0] / magnitude, front_vector[1] / magnitude)

#     # Define an arbitrary "up" direction
#     up_vector = (0, 1)

#     # Compute the cross product between the front and up vectors to get the "right" vector
#     left_vector = (-front_vector[1], front_vector[0])
#     right_magnitude = (left_vector[0]**2 + left_vector[1]**2)**0.5
#     left_vector = (left_vector[0] / right_magnitude, left_vector[1] / right_magnitude)

#     # Compute the cross product between the "right" and front vectors to get the "left" vector
#     right_vector = (front_vector[1], -front_vector[0])
#     left_magnitude = (right_vector[0]**2 + right_vector[1]**2)**0.5
#     right_vector = (right_vector[0] / left_magnitude, right_vector[1] / left_magnitude)

#     return right_vector, left_vector


# print(getRightLeftVectors((0,1)))

# print(getRightLeftVectors((1,0)))

# import math



# def get_position_and_vector(data_list, wheel_diameter = 1/ (math.pi)):
#     position = [0, 0] #the initial position the robot starts at
#     init_dir_vec = [1, 0] #teh vector corrsponding to 0 degrees or 360 degress from gyro, ie the initial direction it is facing
#     dir_vec = []
#     circumference = math.pi * wheel_diameter
#     for data in data_list:
#         # Calculate the distance travelled by each wheel based on the motor values
#         left_distance = data["left_motor"] / 360 * circumference
#         right_distance = data["right_motor"] / 360 * circumference
        
#         # Calculate the total distance travelled and the angle turned
#         total_distance = (left_distance + right_distance) / 2
#         angle = math.radians(data["any_gyroscope"])
        
#         # Update the direction vector based on the angle turned
#         x, y = init_dir_vec
        
#         dir_vec = [x * math.cos(angle) - y * math.sin(angle),
#                             x * math.sin(angle) + y * math.cos(angle)]
#         print(dir_vec)
#         # Update the position based on the total distance travelled and the direction vector
#         position[0] += total_distance * dir_vec[0]
#         position[1] += total_distance * dir_vec[1]
    
#     return position, tuple(dir_vec)

# def convert_to_position_data(input_list, wheel_radius = 1/ (2* math.pi)):
#     position_data = []
#     position = (0, 0)
#     direction_vector = (1, 0)
#     wheel_circumference = 2 * math.pi * wheel_radius
#     for d in input_list:
#         encoder = (d["left_motor"] + d["right_motor"]) / 2
#         gyroscope = d["any_gyroscope"]
#         distance_travelled = encoder / 360 * wheel_circumference
#         angle_turned = math.radians(gyroscope)
#         direction_vector = (
#             math.cos(angle_turned) * direction_vector[0] - math.sin(angle_turned) * direction_vector[1],
#             math.sin(angle_turned) * direction_vector[0] + math.cos(angle_turned) * direction_vector[1]
#         )
#         position = (
#             position[0] + distance_travelled * direction_vector[0],
#             position[1] + distance_travelled * direction_vector[1]
#         )
#         position_data.append((position, direction_vector))
#     return position_data

# print(get_position_and_vector([
#     {"left_motor": 360, "right_motor": 360, "any_gyroscope": 90}, 
#     {"left_motor": 360, "right_motor": 360, "any_gyroscope": 90}, 
#     {"left_motor": 360, "right_motor": 360, "any_gyroscope": -90}, 
#     {"left_motor": 360, "right_motor": 360, "any_gyroscope": 0},
#     {"left_motor": 360, "right_motor": 360, "any_gyroscope": 0},
#     {"left_motor": 360, "right_motor": 360, "any_gyroscope": -45}
#     ]))

# import math


# ##NOTE As u center the front sensor will not be facing where it wants to be, nor will any of the sensors

# ##should only run this while moving in a hallway
# def center(sensor, curr_raw_dir, dir_vec):
#     #centered
#     centered = False

#     # PID gains
#     kp = 0.5
#     ki = 0.1
#     kd = 0.05

#     # Setpoints
#     setpoint = 10  # cm

#     # Error variables
#     error = sensor["left_ultrasonic"] - sensor["right_ultrasonic"]
#     integral_error = 0
#     derivative_error = 0
#     prev_error = 0

#     # Compute PID output
#     integral_error += error
#     derivative_error = error - prev_error
#     output = kp*error + ki*integral_error + kd*derivative_error

#     # Update previous error
#     prev_error = error

#     # Compute the turning angle based on the PID output and sensor values
#     sensor_diff = abs(error)
#     if sensor_diff <= 2:
#         # Ultrasonics are close, use vectorTurn to turn back to ideal direction
#         vecDeg = math.degrees(math.atan2(dir_vec[1], dir_vec[0]))
#         if abs(curr_raw_dir - vecDeg) > 3:
#             turn_angle = round(vecDeg - curr_raw_dir)
#         else:
#             turn_angle = 0

#         centered = True
#     elif sensor_diff <= setpoint:
#         # Small difference, small turn angle
#         turn_angle = round(output)
#     else:
#         # Large difference, large turn angle
#         turn_angle = round(output + kp*sensor_diff)

#     # Use the turn angle to adjust the robot's trajectory
#     #print(turn_angle)
#     turn(turn_angle)

#     # return if the robot is centered
#     return centered

# angle = 90
# turn_angle = center({"left_ultrasonic": 20, "right_ultrasonic": 40}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 25, "right_ultrasonic": 35}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 27, "right_ultrasonic": 33}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 28, "right_ultrasonic": 32}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 30, "right_ultrasonic": 30}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )

# print("get back to cetner")

# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 40, "right_ultrasonic": 20}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 27, "right_ultrasonic": 33}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 28, "right_ultrasonic": 32}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 30, "right_ultrasonic": 30}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )






# turn_angle = center({"left_ultrasonic": 35, "right_ultrasonic": 25}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 40, "right_ultrasonic": 20}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 35, "right_ultrasonic": 25}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 30, "right_ultrasonic": 30}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )
# turn_angle = center({"left_ultrasonic": 30, "right_ultrasonic": 30}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )

# #center({"left_ultrasonic": 40, "right_ultrasonic": 20}, 90, (0,1))



# print("extreme values")
# angle = 90

# turn_angle = center({"left_ultrasonic": 30, "right_ultrasonic": 100}, angle, (0,1))
# angle += turn_angle
# print("im facing: ", angle )