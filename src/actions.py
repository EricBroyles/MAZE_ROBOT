import time
from math import pi
from constants import *
from helpers import getItemByName, getType
from inputs import read

#this applies the inverse to the motor
def setMotorDPS(name, dps, items = ROBOT):
    item = getItemByName(name, items)
    if item is not None:
        LEGO.set_motor_dps(item["port"], -dps if item["inverse"] else dps)
    else:
        print(f"ERROR @startMotor: no item of name: {name} found -> failed to start motor")

def resetEncoders(items = ROBOT):
    for item in items:
        type = getType(item)
        if(type == "motor"):
            LEGO.reset_motor_encoder(item["port"])

#stops all motors
def stop(items = ROBOT):
    for item in items:
        type = getType(item)
        if type == "motor":
            name = item["name"]
            setMotorDPS(name, 0)
            print(f"@stop: stopped motor with name: {name}")


def turn(delta):
    initDegree = read("gyroscope")
    print("@turn: initDegree = ", initDegree)

    target = initDegree + delta
    currDegree = initDegree

    #begin to turn

    #go cw -> right
    if(delta < 0):
        setMotorDPS("left_motor", -TURN_DPS)
        setMotorDPS("right_motor", TURN_DPS)
        while(currDegree > target):
            time.sleep(DELAY / 2)
            currDegree = read("gyroscope")
        
    #go ccw -> left
    elif(delta > 0):
        setMotorDPS("left_motor", TURN_DPS)
        setMotorDPS("right_motor", -TURN_DPS)
        while(currDegree < target):
            time.sleep(DELAY / 2)
            currDegree = read("gyroscope")

    else:
        print("@turn ERROR !!!!! no turn by 0 degree")
        return 0
    
    stop()
    print("@turn: DONE ROTATION -> ", read("gyroscope"), " vs currDegree: ", currDegree, "with initDegree: ", initDegree)


#turns to a desired vector
def vectorTurn(from_angle, to_vector):

    pass





def startMove(dps = MOVE_DPS):
    setMotorDPS("left_motor", dps)
    setMotorDPS("right_motor", dps)

#distance in meters
def move(distance):

    raw_pos = [] #[{"t": , "left_motor": , "right_motor": }, ...]
    
    resetEncoders()
    motorReading = read("motor")
    (currLeftMotorEncoder, currRightMotorEncoder) = (motorReading["left_motor"], motorReading["right_motor"])
    raw_pos.append({"t": time.time(), "left_motor": currLeftMotorEncoder, "right_motor": currRightMotorEncoder})
    finalEncoderVal = 360 * (abs(distance) / (pi * WHEEL_DIA))

    #either 1, or -1 for a reverse
    reverse = -1 if distance < 0 else 1

    startMove(reverse * MOVE_DPS)

    while(abs(currLeftMotorEncoder) <= finalEncoderVal):
        time.sleep(DELAY)
        motorReading = read("motor")
        (currLeftMotorEncoder, currRightMotorEncoder) = (motorReading["left_motor"], motorReading["right_motor"])
        raw_pos.append({"t": time.time(), "left_motor": currLeftMotorEncoder, "right_motor": currRightMotorEncoder})

    print("@MOVE: DONE MOVE -> LEFT: ", read("motor")["left_motor"]  , " RIGHT: ", read("motor")["right_motor"]  )
    
    stop()

    return raw_pos



def pause():
    stop()
    print("PAUSING")
    go = input("enter anything to start again: ")
    return go
