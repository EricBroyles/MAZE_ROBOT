import math


##????????????????????????????????????????????????????????????????????????????????????

def preventOverCenter(req_turn_angle, curr_raw_dir, ideal_dir_vec, center_thresh = 40):
    x, y = ideal_dir_vec
    ideal_angle = math.atan2(y, x)

    #check if the requested turn angle combined with the robots current direction goes beyond the thresh from the ideal
    check = req_turn_angle + curr_raw_dir - ideal_angle 
    if check > center_thresh:
        turn_angle = center_thresh
    elif check < center_thresh:
        turn_angle = -center_thresh
    else:
        turn_angle = req_turn_angle

    return turn_angle


print(preventOverCenter(90, 90, (0,1)))
print(preventOverCenter(-90, 90, (0,1)))

print(preventOverCenter(90, 50, (0,1)))
print(preventOverCenter(-90, 50, (0,1)))

print(preventOverCenter(90, 70, (0,1)))
print(preventOverCenter(-90, 70, (0,1)))