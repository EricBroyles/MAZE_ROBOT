
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

#raw_sensor_data = [{"name": }, ...]
def getFinalPosAndVec(raw_sensor_data, wheel_diameter = WHEEL_DIA):
    position = [0, 0] #the initial position the robot starts at
    init_dir_vec = [1, 0] #teh vector corrsponding to 0 degrees or 360 degress from gyro, ie the initial direction it is facing
    dir_vec = []
    circumference = math.pi * wheel_diameter
    for data in raw_sensor_data:
        # Calculate the distance travelled by each wheel based on the motor values
        left_distance = data["left_motor"] / 360 * circumference
        right_distance = data["right_motor"] / 360 * circumference
        
        # Calculate the total distance travelled and the angle turned
        total_distance = (left_distance + right_distance) / 2
        angle = math.radians(data["any_gyroscope"])
        
        # Update the direction vector based on the angle turned
        x, y = init_dir_vec
        
        dir_vec = [x * math.cos(angle) - y * math.sin(angle),
                            x * math.sin(angle) + y * math.cos(angle)]
        print(dir_vec)
        # Update the position based on the total distance travelled and the direction vector
        position[0] += total_distance * dir_vec[0]
        position[1] += total_distance * dir_vec[1]
    
    return position, tuple(dir_vec)

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
