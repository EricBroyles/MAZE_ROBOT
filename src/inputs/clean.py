from robot import myRobot
from constants import STANDARD_CLEAN


#data gets passed into various helper cleaing fucntions 

#list: [{"type": "", "loc": "", "data": [x,x,x,x]}, ]



##encoder, gyroscope, ultrasonic data should folllow the same algo to clean

#
def clean(type, list):

    cleanData = list.copy()
    if type in STANDARD_CLEAN:
        
        #find the median (not mean as data may have extreme outliers)
        while len(cleanData) > 1:
            if len(cleanData) == 2:
                cleanData = [sum(cleanData) / len(cleanData)]
                break
            cleanData.remove(max(cleanData))
            cleanData.remove(min(cleanData))

    return cleanData[0]
    


##waits until the sensor is not reading invalid data
def initSensorDelay(type, loc):


    pass