##any functions that aid with math around vectors or angles

import math

def angleToVector(angle_deg):
    angle_rad = math.radians(angle_deg)
    x = math.cos(angle_rad)
    y = math.sin(angle_rad)
    return (x, y)

def getDirectionVectors(front_vector):
    x, y = front_vector
    magnitude = (x ** 2 + y ** 2) ** 0.5
    unit_vector = (x / magnitude, y / magnitude)
    cw_vector = (unit_vector[1], -unit_vector[0])
    ccw_vector = (-unit_vector[1], unit_vector[0])
    opposite_vector = (-unit_vector[0], -unit_vector[1])
    
    return {"front": front_vector,"right": cw_vector,"left": ccw_vector,"back": opposite_vector}

def closestAxisVector(vector):
    """
    Returns the direction vector corresponding to the axis that the input vector is closest to.

    Parameters:
        vector (tuple): A 2-dimensional vector in the form (x, y).

    Returns:
        tuple: A 2-dimensional vector in the form (dx, dy) corresponding to the closest axis direction.
    """
    x, y = vector
    dx, dy = 0, 0
    if abs(x) > abs(y):
        dx = 1 if x > 0 else -1
    else:
        dy = 1 if y > 0 else -1
    return (dx, dy)

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