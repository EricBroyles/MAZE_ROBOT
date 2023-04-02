import time
import numpy as np
from constants import *
from helpers import getType

def clean(unclean):

    cleaned = {} 
    copy_unclean = unclean.copy()

    for item in copy_unclean:
        typeItem = getType(item)
        data = None

        if typeItem in MEDIAN_CLEAN:
            data = np.median(item["data"])

        cleaned[item["name"]] = data
        
    return cleaned

#base functions to read all sensors, encoders etc.
##Standard Output {"name": data, ...} or just data if type is specified
def read(type = None, items = ROBOT):

    unclean = []

    for item in items:
        typeItem = getType(item)
        if type is None or type == typeItem:
            item_copy = item.copy()
            item_copy.update({"data": []})
            unclean.append(item_copy)

    dataPts = 0
    while(dataPts < LESS_DATA_PTS):


        for item in unclean:
            typeItem = getType(item)
            reading = None

            if typeItem == "motor":
                
                reading = LEGO.get_motor_encoder(item["port"])

            elif typeItem == "gyroscope":
                
                reading = LEGO.get_sensor(item["port"])

            elif typeItem == "ultrasonic":
                
                reading = GROVE.ultrasonicRead(item["port"])
            
            item["data"].append(reading)
        time.sleep(DELAY)
        dataPts += 1

    

    cleaned = clean(unclean)

    if len(cleaned) == 1:
        for val in cleaned.values():
        
            return val
        
       
    
    return cleaned
