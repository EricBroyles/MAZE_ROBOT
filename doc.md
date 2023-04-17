"""

vector change is a turn by 90, 180, ... etc to target a new vector, can also do small turn to keep robot centered etc..

curr_raw_pos = {"t": , "left_motor": , "right_motor": }
curr_raw_dir = #int, degrees from gyro

NOTE list of lists of encoder data recoreded and added to a list until a vector change is recorded, add this list to all_raw_pos
all_raw_pos = [([{"t": , "left_motor": , "right_motor": }, x5...], curr_raw_gyro), ([{"t": , "left_motor": , "right_motor": }, x20...], curr_raw_gyro), ...]

NOTE curr_raw_gyro converted into a dir_vec
all_pos = [([(x,y,t), 5x...], (x,y)), ([(x,y,t), 5x...], (x,y)), ...]


the maze is made up of path_items and junc_items

NOTE by def a path has been explored

path_items = [
    {
        "is_entr": , #T/F, is this area including the entrance, NOTE DONT ENTER THIS AREA
        "path_trav": , #[(x,y,t), ...] NOTE ROBOT PATH IS EXPECTED TO WOBBLE NOTE ONLY NEED 1st and last item, rest is for debug
        "dir_vec_trav": , #(x,y)
        "hazards": , #[{"type": , "pos": (x, y, t)}, ...]
    }, ...] 

NOTE a junc is defined as any place where their is an option to travel down a path at a different dir_vec than current dir
* on detection create a junc_item for all directions that could be traveled in, including back the way traveled!!!
* the bck the way trav will allow to navigate back out of a dead end area by giving u somthing to target
*when going down an explored junction do not create a path

junc_items = [
    {
        "is_expl": , #T/F, has this junction been traveled down
        "pos_junc": , #(x, y, t), this is shared between all different direction vectors that make up a junc
        "dir_vec_junc": , #(x,y), the direction to travel down the junction
        "uncertain": ,#T/F, if a juncction continues in the direction of travel, it needes to be checked to see if it is a wall
    }, ...]

    


all functions are camelCase, all vars are snake_case
short-hands:
    * pos = position
    * dir = direction
    * vec = vector
    * entr = entrance
    * trav = traveled
    * junc = junction
    * expl = explored



"""