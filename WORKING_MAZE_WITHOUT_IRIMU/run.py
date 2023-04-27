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
            is_junc, is_deadend, is_exit, is_hallway = checkSenarios(all_sensors_data[-1])

            if not(is_hallway):
                print("\n********************************************************************")
                print("NOT IN A HALLWAY ANY MORE is_junc: ", is_junc, "is_deadend: ", is_deadend, "is_exit: ", is_exit)
                stop() # ======= start stop sequence

                real_dir_vec = updateAfterStartStop(all_sensors_data, all_raw_pos, all_pos, do_norm_encoders)

                if is_junc:
                    #want to place the robot towards the center of a junc area
                    is_exit = centerInJunc() # ======== start stop sequence

                    real_dir_vec = updateAfterStartStop(all_sensors_data, all_raw_pos, all_pos, do_norm_encoders)

                #create a junction when it is not the hallway, ie in a deadend, exit, or junc
                curr_junc_id = createJunc(all_sensors_data[-1], all_pos[-1], ideal_dir_vec, junc_items) #adds the item to junc_items

                #found the exit so stop
                if is_exit:
                    found_exit = checkExit()
                    #break

                #choose path to go down, this will set the explored and also set the new ideal dir vector
                new_ideal_dir_vec = choosePath(ideal_dir_vec, curr_junc_id, junc_items)

                if(new_ideal_dir_vec == None):
                    print("OUT of PATH options ERROR")
                    for item in junc_items:
                        print(item)
                
                #turn to this new idea direction vector
                turn_amount = vectorRotation(ideal_dir_vec, new_ideal_dir_vec) #amount to rotate if at ideal dir_vec to get to new dir_vec
                turn(turn_amount)

                #set the actual ideal_dir_vec
                ideal_dir_vec = new_ideal_dir_vec

                #perform a default move of some distance to get out of the junction area
                move(.30) # ====== start stop
                real_dir_vec = updateAfterStartStop(all_sensors_data, all_raw_pos, all_pos, do_norm_encoders)

                #begin moving again
                startMove()

                print("\nDONE NOT Hallway seq: ")
                print("Junctions are currently:")
                for item in junc_items:
                    print("JUNCTION: ", item)
                print("********************************************************************\n")


        stop()
        print("hallway complete")
        #move(.2)
        turn(360)

        print("dumping objects")
        dump()

        

        for item in all_pos:
            print(item)

        for item in junc_items:
            print(item)

        x,y = all_pos[-1]
        print("final position x: ", x * 39.37, y * 39.37)
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

print("END -> RESET")
LEGO.reset_all()
