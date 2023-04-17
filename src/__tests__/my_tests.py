from data import test_sensor_data
from junctions import *
from getFinalPosAndVec import *
from test_helpers import *
from test_map import *

##testing logic to create a juncction

all_pos = [(0,0)]
all_sensors_data = []
ideal_dir_vec = (0, 1) #the y-axis
junc_items = []

#create the entrance junction
#bassically running read here 
all_sensors_data.append(test_sensor_data[0])
junc_id = createJunc(all_sensors_data[-1], all_pos[-1], ideal_dir_vec, junc_items)

for item in test_sensor_data:

    #bassically running read here 
    all_sensors_data.append(item)


    pos, real_dir_vec = getFinalPosAndVec(all_sensors_data, all_pos)
    
    all_pos.append(pos) #run this after any sensors are updated

    #check senario -> junction, dead end, exit, stop the robot if these senarios are encountered
    is_junc, is_deadend, is_exit, is_hallway = checkSenarios(all_sensors_data)

    if not(is_hallway):
        #create a junction when it is not the hallway
        junc_id = createJunc(all_sensors_data[-1], all_pos[-1], ideal_dir_vec, junc_items) #adds the item to junc_items

        #choose path to go down, this will set the explored and also set the new ideal dir vector
        new_ideal_dir_vec = choosePath(junc_id, junc_items)

        #turn to this new idea direction vector

        turn_amount = vectorRotation(real_dir_vec, new_ideal_dir_vec) #amount to rotate if at ideal dir_vec to get to new dir_vec
        #turn(turn_amount)

        #set the actual ideal_dir_vec
        ideal_dir_vec = new_ideal_dir_vec
        print(ideal_dir_vec)

        #perform a default move of some distance to get out of the junction area
        #move(.20) #move by 20 cm


    #if exit is found then break
    if is_exit:
        print("stop exit is found!!!!!!!")
        #stop() #just in case
        #break
    print("\n")
    for item in junc_items:
        print(item)
    print("\n")
my_map = getMap(all_pos)

for row in my_map:
    print(row)
