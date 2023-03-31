from time import time
import numpy as np
from constants import *

def clean(unclean):

    cleaned = unclean.copy

    for item in cleaned:
        type = item.split("_")[-1]

        if type in MEDIAN_CLEAN:
            
            #find the median (not mean as data may have extreme outliers)
            item["data"] = np.median(item["data"])

    return cleaned

#base functions to read all sensors, encoders etc.
##Standard Output [{"name": , "data": int}, ]
def read(items = ROBOT):
    unclean = [{"name": item["name"], "data": []} for item in items]
    # for item in items:
    #     if type in item.keys():
    #         unclean.append({"type": item["type"], "loc": item["loc"], "data": []})

    dataPts = 0
    while(dataPts < LESS_DATA_PTS):

        for item in unclean:
            type = item.split("_")[-1]

            if type == "motor":
                reading = LEGO.get_motor_encoder(item["port"])

            elif type == "gyroscope":
                reading = LEGO.get_sensor(item["port"])

            elif type == "ultrasonic":
                reading = GROVE.ultrasonicRead(item["port"])

            item["data"].append(reading)
        time.sleep(DELAY)
        dataPts += 1

    cleaned = clean(unclean.copy())
    return cleaned