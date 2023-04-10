
import math
from constants import *


def getItemByName(name, arrayDicts = ROBOT):
    """
    Returns the dictionary in array_of_dicts that has a "name" key with the value of name.
    If no dictionary is found with a matching name, returns None.
    """
    for d in arrayDicts:
        if d.get("name") == name:
            return d
        
    print(f"ERROR @getItemBYNAME: no item of name: {name} found")
    return None

def getType(item):
    type = item["name"].split("_")[-1]
    return type
def getLoc(item):
    loc = item["name"].split("_")[0]
    return loc

def angleBetween(v1, v2):
    dot_product = v1[0]*v2[0] + v1[1]*v2[1]
    v1_mag = math.sqrt(v1[0]**2 + v1[1]**2)
    v2_mag = math.sqrt(v2[0]**2 + v2[1]**2)
    cos_angle = dot_product / (v1_mag * v2_mag)
    angle_in_radians = math.acos(cos_angle)
    return math.degrees(angle_in_radians)

#returns the nearest whole num
def vectorRotation(v1, v2):
    angle = angleBetween(v1, v2)
    cross_product = v1[0]*v2[1] - v1[1]*v2[0]
    if cross_product < 0:
        angle = -angle
    return round(angle)

def findClosestVector(angle):
    # Convert angle to radians
    angle_radians = math.radians(angle)

    # Calculate the sine and cosine of the angle
    sin_angle = math.sin(angle_radians)
    cos_angle = math.cos(angle_radians)

    # Determine which axis the angle is closest to based on the signs of sine and cosine
    if abs(sin_angle) > abs(cos_angle):
        if sin_angle > 0:
            #"positive y-axis"
            return (0,1)
        else:
            #"negative y-axis"
            return (0, -1)
    else:
        if cos_angle > 0:
            # "positive x-axis"
            return (1, 0)
        else:
            #"negative x-axis"
            return (-1,0)
        
def encoderToDistance(encoder, wheel_radius = WHEEL_DIA):
    distance = (encoder / 360) * (2 * math.pi * wheel_radius)
    return distance


#raw_sensor: {all sensor readings or just the encoders and gyro} -> must have at lease one item
#all_prev_pos: [(x, y), ....] -> must have at least one item
def getFinalPosAndVec(raw_sensor_data, all_prev_pos, wheel_dia = WHEEL_DIA):

    #error handling
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

# #raw_sensor_data = [{"name": }, ...]
# #returns a single final position and vector reached after some encoder values and gyro readings are recorded
# #assumes robot only moves forawrd, and any encoder change due to a turn is offset before this
# def getFinalPosAndVec(raw_sensor_data, wheel_dia = WHEEL_DIA):
    
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

def getDirectionVectors(front_vector):
    # Ensure that the input vector has unit length
    magnitude = (front_vector[0]**2 + front_vector[1]**2)**0.5
    front_vector = (front_vector[0] / magnitude, front_vector[1] / magnitude)

    # Define an arbitrary "up" direction
    up_vector = (0, 1)

    # Compute the cross product between the front and up vectors to get the "right" vector
    right_vector = (
        front_vector[1] * up_vector[0] - front_vector[0] * up_vector[1],
        front_vector[0] * up_vector[0] + front_vector[1] * up_vector[1]
    )
    right_magnitude = (right_vector[0]**2 + right_vector[1]**2)**0.5
    right_vector = (right_vector[0] / right_magnitude, right_vector[1] / right_magnitude)

    # Compute the cross product between the "right" and front vectors to get the "left" vector
    left_vector = (
        front_vector[0] * up_vector[1] - front_vector[1] * up_vector[0],
        front_vector[0] * up_vector[0] + front_vector[1] * up_vector[1]
    )
    left_magnitude = (left_vector[0]**2 + left_vector[1]**2)**0.5
    left_vector = (left_vector[0] / left_magnitude, left_vector[1] / left_magnitude)

    # Compute the negation of the front vector to get the "back" vector
    back_vector = (-front_vector[0], -front_vector[1])

    return {"front": front_vector,"right": right_vector,"left": left_vector,"back": back_vector}
