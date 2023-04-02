import time
from constants import *
from config import configRobot
from actions import *
from helpers import *


def explore():
    pass


def convertRawToPath(raw_pos, curr_raw_dir, all_pos):
    #raw_pos: [{"t": , "left_motor": , "right_motor": }, ...]
    #curr_raw_dir: int
    #all_pos: [([(x,y,t), 5x...], (x,y)), ([(x,y,t), 5x...], (x,y)), ...]
    #return an item of all_pos ([], ())

    #the final position from the last movement sequence
    final_pos = all_pos[-1][0][-1]

    #the direction vector of the new movement seq
    dir_vec = findClosestVector(curr_raw_dir)

    converted_pos = []

    for raw in raw_pos:
        t = raw["t"]
        left_motor = raw["left_motor"]
        right_motor = raw["right_motor"]
        encoder = (left_motor + right_motor) / 2
        distance = encoderToDistance(encoder)
        converted_pos.append(final_pos[0] + distance * dir_vec[0], final_pos[1] + distance * dir_vec[1], t)

    return (converted_pos, dir_vec)

def updatePathItems(path, path_items, is_entr = False):
    #path: ([(x,y,t), 5x...], (x,y))
    #appends the item to path_items
    path_items.append({"is_entr": is_entr, "path_trav": path[0], "dir_vec_trav": path[1]})


##Time
base_time = time.time()

##MAZE ITEMS
path_items = []
junc_items = []

##SENSORS
all_sens = {}

##POSITION
curr_raw_pos = {}
curr_raw_dir = None
all_raw_pos = []
all_pos = []




##CONFIG
configRobot()


try:
    found_exit = False

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!the robot should start facing the pos x axis!!!!!!!!!!
    #it will now be facing the pos y axis
    turn(90)
    all_pos.append(([0,0, base_time], POS_Y_VEC))

    #create the entrance buffer zone
    curr_raw_dir = read("gyroscope")
    raw_pos = move(ENTR_BUFFER_LEN)
    all_raw_pos.append((raw_pos, curr_raw_dir))

    path = convertRawToPath(raw_pos, curr_raw_dir, all_pos)

    all_pos.append(path)
    is_entr = True
    updatePathItems(path, path_items, is_entr)
    #done creating the entrance buffer zone

    while not(found_exit):

        #explore: only exit this when a dead end or exit is reached
        found_exit = explore(path_items, junc_items, all_raw_pos, )

        if found_exit:
            break

        #find the next closest unexplored junction based on the shortest path to the new junc
        #path_to_junc = findNextJunc(path_items, junc_items)

        #naviagte back to this junction
        #followPath(path_to_junc)
    

    #deploy items

    #create graph

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    print("You pressed ctrl+C...")
