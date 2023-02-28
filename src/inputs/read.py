from main import myRobot
from time import time
from constants import SENSOR_DELAY, NUM_DATA_PTS, LESS_DATA_PTS, GYROSCOPE_XY_IDX
from clean import clean

#base functions to read all sensors, encoders etc.

#pull the data and then have it cleaned

##Standard Output [{"type": "", "loc": "", "data": xxxxxxxxx}, ]

#reads data for all of type motor

#####POTENTIAL PROBLEM, it reads one at a time, ie by the time it gets to the second encoder .1 second has elapsed

def readEncoders():
    unclean = []
    for item in myRobot.ROBOT:
        if "motor" in item.keys():
            unclean.append({"type": item["type"], "loc": item["loc"], "data": []})

    dataPts = 0
    while(dataPts < NUM_DATA_PTS):

        for item in unclean:
            reading = myRobot.lego.get_motor_encoder(item["port"])
            item["data"].append(reading)
        time.sleep(SENSOR_DELAY)
        dataPts += 1

    clean = clean(unclean.copy(), "motor")
    return clean

#reads data for all of type gyroscope
def readGyroscope():
    unclean = []
    for item in myRobot.ROBOT:
        if "gyroscope" in item.keys():
            unclean.append({"type": item["type"], "loc": item["loc"], "data": []})

    dataPts = 0
    while(dataPts < LESS_DATA_PTS):

        for item in unclean:
            reading = myRobot.lego.get_sensor(item["port"])[GYROSCOPE_XY_IDX]
            item["data"].append(reading)
        time.sleep(SENSOR_DELAY)
        dataPts += 1

    clean = clean(unclean.copy(), "gyroscope")
    return clean

#reads data for all of type ultrasonic
def readUltrasonic():

    unclean = []
    for item in myRobot.ROBOT:
        if "gyroscope" in item.keys():
            unclean.append({"type": item["type"], "loc": item["loc"], "data": []})

    dataPts = 0
    while(dataPts < LESS_DATA_PTS):

        for item in unclean:
            reading = myRobot.grove.ultrasonicRead(item["port"])
            item["data"].append(reading)
        time.sleep(SENSOR_DELAY)
        dataPts += 1

    clean = clean(unclean.copy(), "ultrasonic")
    return clean
    