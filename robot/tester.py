import time
import math
from constants import *
from config import configRobot, orientToYAxis
from actions import *
from helpers import *
from inputs import read
from center import *
from navigate import *
from junctions import *
from experiment import *

##CONFIG
configRobot()
test = "read_ultra"
#test = "panic it is broken" # uncomment and rerun to stop runaway code

try:

    if test == "hallway":
        orientToYAxis()
        ideal_dir_vec = (0,1)
        all_sensors_data = []
        found_exit = False
        junc_items = []
        all_pos = [(0,0)]


        #create the entrance junc
        all_sensors_data.append(read())
        junc_id = createJunc(all_sensors_data[-1], all_pos[-1], ideal_dir_vec, junc_items)

        startMove()

        while(not found_exit):
            #update the sensors
            all_sensors_data.append(read())

            #update the position data
            pos, real_dir_vec = getFinalPosAndVec(all_sensors_data, all_pos)
            all_pos.append(pos) #run this after any sensors are updated

            #check if the robot is in a special situation ie deadend, exit, or junction
            is_junc, is_deadend, is_exit, is_hallway = checkSenarios(all_sensors_data[-1])


            print("checksenarios")
            print(all_sensors_data[-1])
            print(is_junc, is_deadend, is_exit, is_hallway)

            if not(is_hallway):
                stop()

                if is_junc:
                    #want to place the robot towards the center of a junc area
                    is_exit = centerInJunc()

                    #update the sensors
                    all_sensors_data.append(read())

                    #update the position data
                    pos, real_dir_vec = getFinalPosAndVec(all_sensors_data, all_pos)
                    all_pos.append(pos) #run this after any sensors are updated
                    
                #create a junction when it is not the hallway, ie in a deadend, exit, or junc
                junc_id, junc_already_exists = createJunc(all_sensors_data[-1], all_pos[-1], ideal_dir_vec, junc_items) #adds the item to junc_items
                
                #found the exit so stop
                if is_exit:
                    found_exit = is_exit
                    break

                #choose path to go down, this will set the explored and also set the new ideal dir vector
                new_ideal_dir_vec = choosePath(junc_id, junc_items)

                ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #when this is none I have no places to go, and need to find another junction
                #if no other junctions exist then an error has occured

                #turn to this new idea direction vector
                turn_amount = vectorRotation(real_dir_vec, new_ideal_dir_vec) #amount to rotate if at ideal dir_vec to get to new dir_vec
                turn(turn_amount)

                #set the actual ideal_dir_vec
                ideal_dir_vec = new_ideal_dir_vec
                print(ideal_dir_vec)

                #perform a default move of some distance to get out of the junction area
                move(.30)
                #begin moving again
                startMove()


        stop()
        print("hallway complete")

        for item in junc_items:
            print(item)

        for item in all_pos:
            print(item)

    if test == "time_to_turn":
        for deg in range(90, 360, 90):
            t = time.time()
            turn(deg)
            print(time.time() - t)
            print(read("gyroscope"))
            pause()

        stop()

    if test == "run_experiment":
        runExperiment("distance_vs_error")

    if test == "encoderval_to_distance":
        left_motor, right_motor = (0,0)
        startMove()
        while abs(left_motor + right_motor) / 2 <= 3800:
            reading = read("motor")
            right_motor = reading['right_motor']
            left_motor = reading['left_motor']
        stop()

    if test == "hallway_center":
        orientToYAxis()
        ideal_dir_vec = (0,1)
        all_sensors_data = []
        found_exit = False

        startMove()

        while(not found_exit):
            sensors = read()
            print(sensors)
            all_sensors_data.append(sensors)
            center(sensors, ideal_dir_vec)
            is_junc, is_deadend, is_exit, is_hallway = checkSenarios(all_sensors_data[-1])
            found_exit = is_exit

        stop()
        print("hallway complete")
    

    if test == "move":
        move(.305)
        pause()
        move(.305)
        pause()
        move(.305)
        pause()
        move(.305)
        stop()
        print(read())
    elif test == "far_move":
        move(.305 * 4)
        pause()
        move(.305 * 2)
        pause()
        move(.305 * 2)
        pause()
        move(.305 * 2)
        stop()
        print(read())
    elif test == "turn":
        turn(90 * 2)
        print("gyro reads: ", read("gyroscope"))
        pause()
        turn(-90 * 2)
        print("gyro reads: ", read("gyroscope"))
        pause()
        turn(90 *2)
        print("gyro reads: ", read("gyroscope"))
        pause()
        turn(-90 *2)
        print("gyro reads: ", read("gyroscope"))
        stop()
    elif test == "read":
        while(True):
            print(read())
            time.sleep(.01)
    elif test == "read_gyro":
        while(True):
            print(read("gyroscope"))
            time.sleep(.01)

    elif test == "read_ultra":
        while(True):
            print(read("ultrasonic"))
            time.sleep(.01)

    elif test == "encoder_dist":

        ##BADD CODE REFERENCE ONLY
        startMove()
        num = 25
        while(num > 0):
            print(read("motor")['right_motor'] , " vs ",  read("motor")['left_motor'])
            num -= 1
        print("FINAL")
        right_motor = read("motor")['right_motor']
        left_motor = read("motor")['left_motor']
        encoder_reading_final = (right_motor + left_motor) / 2
        print("ENCODERS: ", right_motor , " vs ",  left_motor, " vs ", encoder_reading_final)
        c = WHEEL_DIA * math.pi
        rev = encoder_reading_final / 360
        distance_traveled_meters = c * rev
        distance_traveled_inches = distance_traveled_meters * 39.37
        print("Distance traveled: {:.2f} meters, {:.2f} inches".format(distance_traveled_meters, distance_traveled_inches))

        stop()
    elif test == "encoder_diff":
        startMove()
        num = 100
        while(num > 0):
            print(num, " === ", read("motor")['right_motor'] - read("motor")['left_motor'])
            num -= 1
        stop()

    elif test == "ultrasonic_bounds":
        while(True):
            print(read("ultrasonic"))
    else:
        stop()

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    stop()
    print("You pressed ctrl+C...")

print("EXIT COMPLETE reset")
LEGO.reset_all()
