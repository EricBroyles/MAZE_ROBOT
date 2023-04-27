import math
from actions import *
from vectors import *


def findTurnAngle(sensors, ideal_dir_vec):
    centered = False
    turn_angle = 0

    curr_raw_dir = sensors["any_gyroscope"]

    curr_raw_dir_vec = angleToVector(curr_raw_dir)
    curr_angle_cure = vectorRotation(ideal_dir_vec, curr_raw_dir_vec) #how much angle is already being applied to center the robot

    # PID gains
    kp = 0.5
    ki = 0.1
    kd = 0.1

    # Error variables
    error =  sensors["left_ultrasonic"] - sensors["right_ultrasonic"]

    output = kp*error + ki*error + kd*error

    output -= curr_angle_cure

    if(output > 40):
        output = 40
    elif(output < -40):
        output = -40

    turn_angle = output
    
    #when the ultrasonics aree close to another, set back to face the ideal
    if(abs(error) < 10):
        turn_angle = -curr_angle_cure
        centered = True

    return turn_angle, centered

#38 is output for 40cm
# print(findTurnAngle({"left_ultrasonic": 20,"right_ultrasonic": 20, "any_gyroscope": 110}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 20, "any_gyroscope": 110}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 20, "any_gyroscope": 90}, (0,1)))

# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 30, "any_gyroscope": 110}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 30, "any_gyroscope": 90}, (0,1)))

# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 500, "any_gyroscope": 110}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 500, "any_gyroscope": 90}, (0,1)))


# print()
# print(findTurnAngle({"left_ultrasonic": 20,"right_ultrasonic": 20, "any_gyroscope": 70}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 20, "any_gyroscope": 70}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 20, "any_gyroscope": 90}, (0,1)))

# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 30, "any_gyroscope": 70}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 30, "any_gyroscope": 90}, (0,1)))

# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 500, "any_gyroscope": 70}, (0,1)))
# print(findTurnAngle({"left_ultrasonic": 10,"right_ultrasonic": 500, "any_gyroscope": 90}, (0,1)))


##NOTE As u center the front sensor will not be facing where it wants to be, nor will any of the sensors
##should only run this while moving in a hallway, does not work well with extereme values for ultra corresponding
# to junctions
#curr_raw_dir is the raw gyro reading, and dir_vec is the direction the robot should be facing 
#note sensor, should just be the current sensor reading in {} not [{}]
#this should never exceed 45 degrees or 40 degrees away from the center line

##WILL NOT WORK IN A JUNCTION or TURN, will over correct
def center(sensors, ideal_dir_vec):

    turn_made = False
    
    turn_angle, centered = findTurnAngle(sensors, ideal_dir_vec)

    print("@center: ", turn_angle)
    if(turn_angle != 0):
        turn_made = True
        turn(turn_angle, "no_stop")
  
    # return if the robot is centered
    return centered, turn_made

# def centerInJunc(contact_thresh = CONTACT_ULTRA_THRESH, space_thresh = SPACE_ULTRA_THRESH, wide_open_thresh = WIDE_OPEN_ULTRA_THRESH):

#     print("\n+++++++++++++++++++++++++++++++++++++++++++++")
#     print("Begin to center")

#     is_exit = False
#     num_wide_open_spikes = 0
#     edge_junc_found = False #become true when 20 < ultra_diff < wide_open_ultra

#     sensors = read()
#     prev_left_motor = sensors["left_motor"]
#     prev_right_motor = sensors["right_motor"]
#     prev_left = sensors["left_ultrasonic"]
#     prev_right = sensors["right_ultrasonic"]

#     contact_front = True if sensors["front_ultrasonic"] <= contact_thresh else False

#     curr_left = prev_left
#     curr_right = prev_right

#     startMove(SLOW_LEFT_MOVE_DPS, SLOW_RIGHT_MOVE_DPS)



#     #if at any point an exit or a wall in front is encountered then done
#     #if 3 large spikes of magnitdue greater or equal to wide_open_thresh are encountered then, the second one is the center, no reverse needed
#     #if first negetive spike is greater than 20 but less than wide_open, you have found the edge of the junction area, reverse for half the distance traveled to be in the center

#     while num_wide_open_spikes < 2:

#         sensors = fastRead("ultrasonic")
#         curr_front = sensors["front_ultrasonic"]
#         curr_left = sensors["left_ultrasonic"]
#         curr_right = sensors["right_ultrasonic"]

#         delta_left = curr_left - prev_left 
#         delta_right = curr_right - prev_right

#         print("@center: curr_left: ", curr_left, "prev_left: ", prev_left, "delta_left: ", delta_left)
#         print("@center: curr_right: ", curr_right, "prev_right: ", prev_right, "delta_right: ", delta_right)

#         space_front = True if curr_front > space_thresh else False
#         space_left  = True if curr_left > space_thresh else False
#         space_right = True if curr_right > space_thresh else False

#         is_exit = True if space_front and space_left and space_right else False

#         contact_front = True if sensors["front_ultrasonic"] <= contact_thresh else False

#         #kill this if every detect a wall in front, or finds the exit
#         if is_exit or contact_front:
#             break

#         #should be strictly negetive delta being considered
#         if delta_left <= -20 and delta_left >= -wide_open_thresh or delta_right <= -20 and delta_right >= -wide_open_thresh:
#             edge_junc_found = True
#             break 

#         if abs(delta_left) >= wide_open_thresh or abs(delta_right) >= wide_open_thresh:
#             num_wide_open_spikes += 1

#         print("num_wide_open_spikes", num_wide_open_spikes)

#         prev_left = curr_left
#         prev_right = curr_right

#     stop()
#     if not (is_exit or contact_front) and edge_junc_found:
#         sensors = read("motor")
#         curr_left_motor = sensors["left_motor"]
#         curr_right_motor = sensors["right_motor"]

#         center_target_delta = ((curr_left_motor + curr_right_motor) / 2 - (prev_left_motor + prev_right_motor) / 2) / 2
#         center_targer_encoder =  (prev_left_motor + prev_right_motor) / 2 + center_target_delta

#         startMove(-SLOW_LEFT_MOVE_DPS, -SLOW_RIGHT_MOVE_DPS)

#         while (curr_right_motor + curr_left_motor) / 2 < center_targer_encoder:
#             sensors = read("motor")
#             curr_left_motor = sensors["left_motor"]
#             curr_right_motor = sensors["right_motor"]
        

#     print("PAUSING FOR JUNCTION CENTER COMPLETE")
#     pause()

#     print("+++++++++++++++++++++++++++++++++++++++++++++\n")

#     return is_exit 









# def centerInJunc(contact_thresh = CONTACT_ULTRA_THRESH, space_thresh = SPACE_ULTRA_THRESH):

#     print("\n+++++++++++++++++++++++++++++++++++++++++++++")
#     print("Begin to center")

#     graph_left = []
#     graph_right = []
#     graph_delta_left = [0]
#     graph_delta_right = [0]

#     is_exit = False
#     num_spikes = 0

#     sensors = read()
#     prev_left_motor = sensors["left_motor"]
#     prev_right_motor = sensors["right_motor"]
#     prev_left = sensors["left_ultrasonic"]
#     prev_right = sensors["right_ultrasonic"]

#     contact_front = True if sensors["front_ultrasonic"] <= contact_thresh else False

#     curr_left = prev_left
#     curr_right = prev_right

#     graph_left.append(curr_left)
#     graph_right.append(curr_right)

#     startMove(SLOW_LEFT_MOVE_DPS, SLOW_RIGHT_MOVE_DPS)

#     while num_spikes <= 2:

#         sensors = fastRead("ultrasonic")
#         curr_front = sensors["front_ultrasonic"]
#         curr_left = sensors["left_ultrasonic"]
#         curr_right = sensors["right_ultrasonic"]

#         graph_left.append(curr_left)
#         graph_right.append(curr_right)
#         graph_delta_left.append(curr_left - prev_left)
#         graph_delta_right.append(curr_right - prev_right)



#         print("@center: curr_left: ", curr_left, "prev_left: ", prev_left, "delta_left: ", curr_left - prev_left)
#         print("@center: curr_right: ", curr_right, "prev_right: ", prev_right, "delta_right: ", curr_right - prev_right)

#         space_front = True if curr_front > space_thresh else False
#         space_left  = True if curr_left > space_thresh else False
#         space_right = True if curr_right > space_thresh else False

#         is_exit = True if space_front and space_left and space_right else False

#         contact_front = True if sensors["front_ultrasonic"] <= contact_thresh else False

#         #kill this if every detect a wall in front, or finds the exit
#         if is_exit or contact_front:
#             break

#         if abs(curr_left - prev_left) >= 20 or abs(curr_right - prev_right) >= 20:
#             num_spikes += 1

#         print("num_spikes", num_spikes)

#         prev_left = curr_left
#         prev_right = curr_right

#     stop()
#     # if not (is_exit or contact_front):
#     #     sensors = read("motor")
#     #     curr_left_motor = sensors["left_motor"]
#     #     curr_right_motor = sensors["right_motor"]

#     #     center_target_delta = ((curr_left_motor + curr_right_motor) / 2 - (prev_left_motor + prev_right_motor) / 2) / 2
#     #     center_targer_encoder =  (prev_left_motor + prev_right_motor) / 2 + center_target_delta

#     #     startMove(-SLOW_LEFT_MOVE_DPS, -SLOW_RIGHT_MOVE_DPS)

#     #     while (curr_right_motor + curr_left_motor) / 2 < center_targer_encoder:
#     #         sensors = read("motor")
#     #         curr_left_motor = sensors["left_motor"]
#     #         curr_right_motor = sensors["right_motor"]
        

#     print("PAUSING FOR JUNCTION CENTER COMPLETE")
#     pause()

    



#     x = list(range(1, len(graph_left) + 1))
    

#     # Create a figure and axis object
#     fig, ax = plt.subplots()

#     # Plot the first dataset (array of numbers)
#     ax.plot(x, graph_left, label='left reading')
#     ax.plot(x, graph_right, label='right reading')
#     ax.plot(x, graph_delta_left, label='left delta reading')
#     ax.plot(x, graph_delta_right, label='right delta reading')

#     # Set axis labels and title
#     ax.set_xlabel('X')
#     ax.set_ylabel('value')
#     ax.set_title('Centering in Junction Ultrasonic Readings')

#     # Add a legend
#     ax.legend()

#     # Show the plot
#     plt.show()

#     print("+++++++++++++++++++++++++++++++++++++++++++++\n")


#     return is_exit 