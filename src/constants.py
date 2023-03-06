##CONSTANTS

##Coordinate System
INIT_X_POS = 0
INIT_Y_POS = 0 

#the size of the wheel in m
WHEEL_DIA = 0.05556504 #meters

#max run time for config a sensor before somthing is probably wrong with the sensor
MAX_SENSOR_CONFIG_TIME = 5 #seconds


#amount of time (s) between getting data from any robot item (sensor/encoder)
DELAY = .01

#the amount of time the sensors will gather data for
SENSOR_READ_TIME = .1


#the number of items to get when fetching data from any robot item (sensor/encoder)
NUM_DATA_PTS = SENSOR_READ_TIME / DELAY

##collect fewer data points for sensors less sensitive to slight fluctuations
LESS_DATA_PTS = round(NUM_DATA_PTS / 2)


#the data pulled from the gyroscope comes in [xy, xz]
GYROSCOPE_XY_IDX = 0

#all items to have data proccessed the same way
STANDARD_CLEAN = ["motor", "gyroscope", "ultrasonic"]



