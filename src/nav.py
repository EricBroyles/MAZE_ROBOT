import math
from actions import *
from helpers import *
from inputs import *

##NOTE As u center the front sensor will not be facing where it wants to be, nor will any of the sensors
##should only run this while moving in a hallway, does not work well with extereme values for ultra corresponding
# to junctions
#curr_raw_dir is the raw gyro reading, and dir_vec is the direction the robot should be facing 
#note sensor, should just be the current sensor reading in {} not [{}]
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
    #print(turn_angle)
    if(turn_angle != 0):
        turnMade = True
        turn(turn_angle)

    # return if the robot is centered
    return centered, turnMade


# def createJuncItem(all_sens, ):



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