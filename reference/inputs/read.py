from main import myRobot
from time import time
from constants import DELAY, NUM_DATA_PTS, LESS_DATA_PTS, GYROSCOPE_XY_IDX
from clean import clean

#base functions to read all sensors, encoders etc.
##Standard Output [{"type": "", "loc": "", "data": xxxxxxxxx}, ]
def read(items, type):
    unclean = []
    for item in items:
        if type in item.keys():
            unclean.append({"type": item["type"], "loc": item["loc"], "data": []})

    dataPts = 0
    while(dataPts < LESS_DATA_PTS):

        for item in unclean:

            if type == "motor":
                reading = myRobot.lego.get_motor_encoder(item["port"])

            elif type == "gyroscope":
                reading = myRobot.lego.get_sensor(item["port"])[GYROSCOPE_XY_IDX]

            elif type == "ultrasonic":
                reading = myRobot.grove.ultrasonicRead(item["port"])

            item["data"].append(reading)
        time.sleep(DELAY)
        dataPts += 1

    cleaned = clean(unclean.copy(), type)
    return cleaned
    
    
#reads data for all of type motor
def readEncoders(items):
    return read(items, "motor")

#reads data for all of type gyroscope
def readGyroscope(items):
    return read(items, "gyroscope")

#reads data for all of type ultrasonic
def readUltrasonic(items):
    return read(items, "ultrasonic")

