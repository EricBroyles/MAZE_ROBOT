import time
from math import pi
from constants import *
from helpers import getItemByName, getLocType
from inputs import fastRead, read

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


def centerInJunc(contact_thresh = CONTACT_ULTRA_THRESH, space_thresh = SPACE_ULTRA_THRESH):

    is_exit = False
    
    sensors = read()
    prev_left = sensors["left_ultrasonic"]
    prev_right = sensors["right_ultrasonic"]

    contact_front = True if sensors["front_ultrasonic"] <= contact_thresh else False
    increasing = True

    if(contact_front):
        stop()
        return 
    
    startMove(SLOW_LEFT_MOVE_DPS, SLOW_RIGHT_MOVE_DPS)

    while not(contact_front) and increasing:
        sensors = read()
        curr_front = sensors["front_ultrasonic"]
        curr_left = sensors["left_ultrasonic"]
        curr_right = sensors["right_ultrasonic"]

        space_front = True if curr_front > space_thresh else False
        space_left  = True if curr_left > space_thresh else False
        space_right = True if curr_right > space_thresh else False

        if space_front and space_right and space_left:
            #exit = all sensor are seeing open space
            is_exit = True
            break

        contact_front = True if sensors["front_ultrasonic"] <= contact_thresh else False
        if(curr_left >= prev_left or curr_right >= prev_right):
            increasing = True

        prev_left = curr_left
        prev_right = curr_right

    stop()

    return is_exit


def pause():
    stop()
    print("PAUSING")
    go = input("enter anything to start again: ")
    return go
