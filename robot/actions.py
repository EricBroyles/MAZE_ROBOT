import time
from math import pi
from constants import *
from helpers import getItemByName, getLocType
from inputs import fastRead, read
from navigate import checkSenarios

#this applies the inverse to the motor
def setMotorDPS(name, dps, items = ROBOT):
    item = getItemByName(name, items)
    if item is not None:
        LEGO.set_motor_dps(item["port"], -dps if item["inverse"] else dps)
    else:
        print(f"ERROR @startMotor: no item of name: {name} found -> failed to start motor")

def startMove(left_dps = LEFT_MOVE_DPS, right_dps = RIGHT_MOVE_DPS):
    setMotorDPS("left_motor", left_dps)
    setMotorDPS("right_motor", right_dps)

def resetEncoders(items = ROBOT):
    for item in items:
        loc, type = getLocType(item)
        if(type == "motor"):
            LEGO.reset_motor_encoder(item["port"])

#stops all motors
def stop(items = ROBOT):
    for item in items:
        loc, type = getLocType(item)
        if type == "motor":
            name = item["name"]
            setMotorDPS(name, 0)

    print("@stop: complete")
            #print(f"@stop: stopped motor with name: {name}")

def turn(delta, type = "controlled"):

    initDegree = read("gyroscope")

    target = initDegree + delta
    currDegree = initDegree

    initEncoders = read("motor") #{"left_motor":, "right_motor": }

    delay = round(int(abs(delta)) / 90) * TIME_TO_TURN_90 * BEGIN_READING_AFTER
    
    #go cw -> right
    if(delta < 0):
        setMotorDPS("left_motor", LEFT_TURN_DPS)
        setMotorDPS("right_motor", -RIGHT_TURN_DPS)
        time.sleep(delay)
        while(currDegree > target):
            currDegree = read("gyroscope")

    #go ccw -> left
    elif(delta > 0):
        setMotorDPS("left_motor", -LEFT_TURN_DPS)
        setMotorDPS("right_motor", RIGHT_TURN_DPS)
        time.sleep(delay)
        while(currDegree < target):
            currDegree = read("gyroscope")
        
    else:
        print("@turn ERROR !!!!! no turn by 0 degree")
        return 0
    
    finalEncoders = read("motor")
        
    LEGO.offset_motor_encoder(getItemByName('left_motor')['port'], finalEncoders['left_motor'] - initEncoders['left_motor'])
    LEGO.offset_motor_encoder(getItemByName('right_motor')['port'], finalEncoders['right_motor'] - initEncoders['right_motor'])
    
    if(type == "controlled"):
        stop()
    print("@turn done -> turn by ", delta)
    #print("@turn: DONE ROTATION -> ", read("gyroscope"), " vs currDegree: ", currDegree, "with initDegree: ", initDegree)

#distance in meters,
#distance must be positive
def move(distance):

    distance = abs(distance)

    motor_reading = read("motor") #get the most accurate reading
    (left_motor, right_motor) = (motor_reading["left_motor"], motor_reading["right_motor"])
    final_encoder_val = 360 * (abs(distance) / (pi * WHEEL_DIA)) + (abs(right_motor) + abs(left_motor)) / 2

    startMove(LEFT_MOVE_DPS, RIGHT_MOVE_DPS)

    while((abs(right_motor) + abs(left_motor)) / 2 <= final_encoder_val):
        #time.sleep(DELAY)
        motor_reading = fastRead("motor")
        (left_motor, right_motor) = (motor_reading["left_motor"], motor_reading["right_motor"])

    print(f"@move: complete -> (left: ", read("motor")["left_motor"], ", right: " , read("motor")["right_motor"], ")")

    #print("@MOVE: DONE MOVE -> LEFT: ", read("motor")["left_motor"]  , " RIGHT: ", read("motor")["right_motor"], " vs: ", final_encoder_val )
    
    stop()

#only is entered once a junction is detected
#continue moving forward until the ultrasonic pointing in the direction of the junc begins to decrease
#or until the front sensor gets close to a wall
#or until it realizes it has exited the maze

def centerInJunc(contact_thresh = CONTACT_ULTRA_THRESH, space_thresh = SPACE_ULTRA_THRESH, wide_open_thresh = WIDE_OPEN_ULTRA_THRESH):

    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Begin to center")

    is_exit = True
    # open_space_spike = False
    edge_junc_found = False 

    sensors = read()
    prev_left_motor = sensors["left_motor"]
    prev_right_motor = sensors["right_motor"]
    prev_left = sensors["left_ultrasonic"]
    prev_right = sensors["right_ultrasonic"]

    hazard_front = True if abs(sensors['front_magnet']['y']) >= FRONT_MAGNET_THRESH or sensors['front_ir'] >= IR_THRESH else False
    contact_front = True if sensors["front_ultrasonic"] <= contact_thresh or hazard_front else False
    print("@center", hazard_front)


    curr_left = prev_left
    curr_right = prev_right

    startMove(SLOW_LEFT_MOVE_DPS, SLOW_RIGHT_MOVE_DPS)

    #stop when seeing the exit, or front sensor in contact with the wall
    #stop when no longer seeding a junction from one of the sensors, perform a reverse
    #stop when experience a large positive spike in ultra reading

    while not edge_junc_found:

        sensors = read()
        curr_front = sensors["front_ultrasonic"]
        curr_left = sensors["left_ultrasonic"]
        curr_right = sensors["right_ultrasonic"]

        delta_left = curr_left - prev_left 
        delta_right = curr_right - prev_right

        print("@center: curr_left: ", curr_left, "prev_left: ", prev_left, "delta_left: ", delta_left)
        print("@center: curr_right: ", curr_right, "prev_right: ", prev_right, "delta_right: ", delta_right)

        space_front = True if curr_front > space_thresh else False
        space_left  = True if curr_left > space_thresh else False
        space_right = True if curr_right > space_thresh else False

        is_exit = True if space_front and space_left and space_right else False
        hazard_front = True if abs(sensors['front_magnet']['y']) >= FRONT_MAGNET_THRESH or sensors['front_ir'] >= IR_THRESH else False
        print("@center", hazard_front)

        contact_front = True if sensors["front_ultrasonic"] <= contact_thresh or hazard_front else False

        edge_junc_found = True if not (space_left or space_right) else False

        #kill this if every detect a wall in front, or finds the exit
        if is_exit or contact_front or edge_junc_found:
            break

        #should be strictly negetive delta being considered
        # if delta_left >= 20 or delta_right >= 20:
        #     open_space_spike = True
        #     break 

        prev_left = curr_left
        prev_right = curr_right

    stop()
    if not (is_exit or contact_front) and edge_junc_found:
        sensors = read("motor")
        curr_left_motor = sensors["left_motor"]
        curr_right_motor = sensors["right_motor"]

        center_target_delta = ((curr_left_motor + curr_right_motor) / 2 - (prev_left_motor + prev_right_motor) / 2) / 2
        center_target_encoder =  (prev_left_motor + prev_right_motor) / 2 + center_target_delta

        startMove(-SLOW_LEFT_MOVE_DPS, -SLOW_RIGHT_MOVE_DPS)

        while (curr_right_motor + curr_left_motor) / 2 <= center_target_encoder:
            sensors = read("motor")
            curr_left_motor = sensors["left_motor"]
            curr_right_motor = sensors["right_motor"]
        

    # print("PAUSING FOR JUNCTION CENTER COMPLETE")
    # pause()

    print("+++++++++++++++++++++++++++++++++++++++++++++\n")

    return is_exit 

def checkExit():
    print("@checkExit")
    sensors = read("motor")
    prev_left_motor = sensors["left_motor"]
    prev_right_motor = sensors["right_motor"]
    move(.40)
    is_junc, is_deadend, is_exit, is_hallway, is_hazard, is_collision, hazard_front = checkSenarios(read())
    if not is_exit:
        print("PAY ATTENTION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Reverseing")
        sensors = read("motor")
        curr_left_motor = sensors["left_motor"]
        curr_right_motor = sensors["right_motor"]

        startMove(-SLOW_LEFT_MOVE_DPS, -SLOW_RIGHT_MOVE_DPS)

        while (curr_right_motor + curr_left_motor) / 2 <= (prev_left_motor + prev_right_motor) / 2:
            sensors = read("motor")
            curr_left_motor = sensors["left_motor"]
            curr_right_motor = sensors["right_motor"]

    print("Done check exit and possibly a reverse")
        
    return is_exit

def pause():
    stop()
    print("PAUSING")
    go = input("enter anything to start again: ")
    return go


def dump(dps = DUMP_DPS):
    """
    push the back gate to drop the item off the back
    """

    #turn the gate until the encoder is 90, wait then turn back the 90

    print("@DUMP -> begining to dump make sure that it is not pushing the wrong way")
    print("@DUMP -> MAKE SURE NO WIRES ARE INTERFFERING")
    # pause()

    item = getItemByName('back_gate')

    print(item)

    gate_dps = -dps if item["inverse"] else dps

    LEGO.reset_motor_encoder(item["port"])
    LEGO.set_motor_dps(item["port"], gate_dps)

    gate_encoder = read("gate")
    while(abs(gate_encoder) < 80):
        gate_encoder = read("gate")

    time.sleep(1)

    #item has now been dumped

    LEGO.reset_motor_encoder(item["port"])
    LEGO.set_motor_dps(item["port"], -gate_dps)

    gate_encoder = read("gate")
    while(abs(gate_encoder) < 85):
        gate_encoder = read("gate")

#does not decide if a panic center is needed, only amends the issue
def panicCenter(contact_thresh = CONTACT_ULTRA_THRESH):
    reading = read("ultrasonic")
    left_ultra = reading["left_ultrasonic"]
    right_ultra = reading["right_ultrasonic"]

    if left_ultra < right_ultra:
        turn_amount = -90
    elif left_ultra > right_ultra:
        turn_amount = 90

    turn(turn_amount)
    #move until the robot sees contact in front and then stop and turn by 90
    startMove(SLOW_LEFT_MOVE_DPS, SLOW_RIGHT_MOVE_DPS)
    contact_front = True if reading["front_ultrasonic"] <= contact_thresh else False
    while not contact_front:
        reading = read("ultrasonic")
        contact_front = True if reading["front_ultrasonic"] <= contact_thresh else False  
    stop()
    turn(-turn_amount)          


