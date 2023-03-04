import math

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

