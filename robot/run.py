from constants import *
from config import configRobot, orientToYAxis
from actions import *
from helpers import *
from inputs import read
from navigate import *
from junctions import *
from update import *
from map import getMap

##CONFIG
configRobot()
kill = "removealltexttostoprunnawayrobot"

try:
    if kill != "":

        ##Vars
        junc_items = []
        all_sensors_data = []
        all_pos = [(0,0)]
        ideal_dir_vec = (0,1)
        real_dir_vec = (0,1)
        curr_junc_id = 1 #the starting junction id, note this is the id of junction the robot is at, not simply a increasing id num
        found_exit = False
        do_norm_encoders = True
        hazards = {} #"magnet": (2,1), "heat": (0, .5)
        hazard_params = {}
        filename = "matrix.csv"

        #will have all the dictionaries sensor items but only needs the 3 listed below
        all_raw_pos = [{"left_motor": 0 , "right_motor": 0, "any_gyroscope": read("gyroscope")}]#[{"left_motor":  , "right_motor"}] only gets updated with the current encoder readings after a start and stop sequence


        ##CONFIG
        configRobot()
        orientToYAxis()
        
        #create the entrance junc
        all_sensors_data.append(read())
        curr_junc_id = createJunc(all_sensors_data[-1], all_pos[-1], ideal_dir_vec, junc_items)
        ans = input("NOTIFY: PERFORMING A DEFULAT MOVE ON CONFIG (y/n)")
        if ans == "y":
            move(.3) # == stop start
            real_dir_vec = updateAfterStartStop(all_sensors_data, all_raw_pos, all_pos, do_norm_encoders)
        startMove()

        while(not found_exit):
            #update the sensors
            all_sensors_data.append(read())

            #check if the robot is in a special situation ie deadend, exit, or junction
            print("checking the scenario")
            is_junc, is_deadend, is_exit, is_hallway, is_hazard, is_collision, hazard_front = checkSenarios(all_sensors_data[-1])
            print(is_junc, is_deadend, is_exit, is_hallway, is_hazard, is_collision)
            if is_collision and is_hallway:
                print("panic center")
                panicCenter()
                startMove()

            if is_hazard or hazard_front:
                print("hazard")
                updateHazards(all_sensors_data[-1], all_pos[-1], hazards, hazard_params)

            if not(is_hallway):
                print("\n********************************************************************")
                print("NOT IN A HALLWAY ANY MORE is_junc: ", is_junc, "is_deadend: ", is_deadend, "is_exit: ", is_exit)
                stop() # ======= start stop sequence

                real_dir_vec = updateAfterStartStop(all_sensors_data, all_raw_pos, all_pos, do_norm_encoders)

                if is_junc:
                    #want to place the robot towards the center of a junc area
                    is_exit = centerInJunc() # ======== start stop sequence

                    real_dir_vec = updateAfterStartStop(all_sensors_data, all_raw_pos, all_pos, do_norm_encoders)
                    updateHazards(all_sensors_data[-1], all_pos[-1], hazards, hazard_params)
                    

                #create a junction when it is not the hallway, ie in a deadend, exit, or junc
                curr_junc_id = createJunc(all_sensors_data[-1], all_pos[-1], ideal_dir_vec, junc_items) #adds the item to junc_items

                #found the exit so stop
                if is_exit:
                    found_exit = checkExit()
                    if found_exit:
                        break

                #choose path to go down, this will set the explored and also set the new ideal dir vector
                new_ideal_dir_vec = choosePath(ideal_dir_vec, curr_junc_id, junc_items)

                while new_ideal_dir_vec is not None:
                    #turn to this new idea direction vector
                    turn_amount = vectorRotation(ideal_dir_vec, new_ideal_dir_vec) #amount to rotate if at ideal dir_vec to get to new dir_vec
                    turn(turn_amount)

                    #set the actual ideal_dir_vec
                    ideal_dir_vec = new_ideal_dir_vec

                    #does a hazard exist in front of the robot
                    curr_sensors = read()
                    hazard_front = True if curr_sensors['front_magnet']['y'] >= FRONT_MAGNET_THRESH or curr_sensors['front_ir'] >= IR_THRESH else False

                    print("IMPORTANT", hazard_front)

                    if not hazard_front:
                        #perform a default move of some distance to get out of the junction are
                        move(.30) # ====== start stop
                        real_dir_vec = updateAfterStartStop(all_sensors_data, all_raw_pos, all_pos, do_norm_encoders)
                        break
                    else:
                        updateHazards(all_sensors_data[-1], all_pos[-1], hazards, hazard_params)
                        

                    new_ideal_dir_vec = choosePath(ideal_dir_vec, curr_junc_id, junc_items)

                if(new_ideal_dir_vec == None):
                    print("OUT of PATH options ERROR")
                    for item in junc_items:
                        print(item)
                
                #begin moving again
                startMove()

                print("\nDONE NOT Hallway seq: ")
                print("Junctions are currently:")
                for item in junc_items:
                    print("JUNCTION: ", item)
                print("********************************************************************\n")


        stop()
        print("MAZE COMPLETE")
        turn(360)
        dump()

        for item in all_pos:
            print(item)

        for item in junc_items:
            print(item)

        x,y = all_pos[-1]
        print("final position x: ", x * 39.37, y * 39.37)
        print(hazards)
        print(hazard_params)
        my_map = getMap(filename, all_pos, hazards)
        for r in my_map:
            print(r)
       
    stop()

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    stop()
    print("You pressed ctrl+C...")

    ans = input("RUN EXIT SEQUENCE (y/n)")
    if ans == "y":
        turn(360)
        dump()
        for item in all_pos:
            print(item)

        for item in junc_items:
            print(item)

        x,y = all_pos[-1]
        print("final position x: ", x * 39.37, y * 39.37)

        print(hazards)
        print(hazard_params)
        my_map = getMap(filename, all_pos, hazards)
        for r in my_map:
            print(r)
       
    


print("END -> RESET")
LEGO.reset_all()
