import time
from constants import LEGO, LEGO_ITEMS, PWR, DELAY

def turn(delta, pwr = PWR):

    initDegree = LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"])
    print("@turn: initDegree = ", initDegree)

    target = initDegree + delta
    currDegree = initDegree

    #begin to turn

    #go cw -> right
    if(delta < 0):
        LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], pwr)
        LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], -pwr)
        while(currDegree > target):
            time.sleep(DELAY / 2)
            currDegree = LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"])
            #print("currDegree ", currDegree)
        
    #go ccw -> left
    elif(delta > 0):
        LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], -pwr)
        LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], pwr)
        while(currDegree < target):
            time.sleep(DELAY / 2)
            currDegree = LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"])
            #print("currDegree ", currDegree)
    else:
        print("@turn ERROR !!!!! no turn by 0 degree")
        return 0

    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_LEFT"], 0)
    LEGO.set_motor_power(LEGO_ITEMS["MOTOR_RIGHT"], 0)
    print("@turn: done with ROTATION: ", LEGO.get_sensor(LEGO_ITEMS["EV3_GYRO"]), " vs currDegree: ", currDegree, "with initDegree: ", initDegree)