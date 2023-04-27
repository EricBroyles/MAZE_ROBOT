import time
import numpy as np
from constants import *
from helpers import getLocType

def clean(unclean):
    cleaned = {} 
    copy_unclean = unclean.copy()

    for item in copy_unclean:
        loc, typeItem = getLocType(item)
        data = item["data"]

        if typeItem in MEDIAN_CLEAN:
            if typeItem == "magnet":
                #{x: , y: , z:}
                x = []
                y = []
                z = []
                for magnet in item["data"]: 
                    for key, val in magnet.items():
                        if key == "x":
                            x.append(val)
                        elif key == "y":
                            y.append(val)
                        elif key == "z":
                            z.append(val)
                    
                    data = {"x": abs(np.average(x)), 'y': abs(np.average(y)), 'z': abs(np.average(z))}
            else:
                data = np.median(item["data"])
        

        cleaned[item["name"]] = data
        
    return cleaned

#base functions to read all sensors, encoders etc.
##Standard Output {"name": data, ...} or just data if type is specified
def read(type = None, items = ROBOT):
    unclean = []

    for item in items:
        loc, typeItem = getLocType(item)
        if type is None or type == typeItem:
            item_copy = item.copy()
            item_copy.update({"data": []})
            unclean.append(item_copy)

    dataPts = 0
    while(dataPts < LESS_DATA_PTS):

        for item in unclean:
            loc, typeItem = getLocType(item)
            reading = None

            if typeItem == "motor":
                reading = LEGO.get_motor_encoder(item["port"])
            elif typeItem == "gate":
                reading = LEGO.get_motor_encoder(item["port"])
            elif typeItem == "gyroscope":
                reading = LEGO.get_sensor(item["port"])
            elif typeItem == "ultrasonic":
                reading = GROVE.ultrasonicRead(item["port"])
            elif typeItem == "magnet":
                reading = MPU.readMagnet()
            elif typeItem == "ir":
                reading = GROVE.analogRead(item["port"])
            
            item["data"].append(reading)

        time.sleep(DELAY / 10)
        dataPts += 1

    cleaned = clean(unclean)

    if len(cleaned) == 1:
        for val in cleaned.values():
            return val
        
    return cleaned


def fastRead(type, items = ROBOT):
    """
    no cleaning is performed!!!!!
    """
    reading = {}

    for item in items:
        loc, typeItem = getLocType(item)
        if type == typeItem:
            if typeItem == "motor":
                reading[item['name']] = LEGO.get_motor_encoder(item["port"])
            elif typeItem == "gyroscope":
                reading[item['name']] = LEGO.get_sensor(item["port"])
            elif typeItem == "ultrasonic":
                reading[item['name']] = GROVE.ultrasonicRead(item["port"])
        time.sleep(DELAY / 10)
        
    return reading
