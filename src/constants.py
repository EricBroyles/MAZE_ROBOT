import lib.brickpi3 as bp
import lib.grovepi as grove

##CONSTANTS
#Coordinate System
INIT_X_POS = 0
INIT_Y_POS = 0 

#the initial direction
POS_Y_VEC = (0, 1)

#the size of the wheel in m
WHEEL_DIA = 0.05556504 #meters

TURN_DPS = 180 #the dps the robot will atempt to turn at
MOVE_DPS = 180 #the dps the robot will atempt to travel at

#max run time for config a sensor before somthing is probably wrong with the sensor
MAX_SENSOR_CONFIG_TIME = 5 #seconds

#amount of time (s) between getting data from any robot item (sensor/encoder)
DELAY = .01
MICRO_DELAY = .005

#the amount of time the sensors will gather data for
SENSOR_READ_TIME = .1

#the number of items to get when fetching data from any robot item (sensor/encoder)
NUM_DATA_PTS = SENSOR_READ_TIME / DELAY

##collect fewer data points for sensors less sensitive to slight fluctuations
LESS_DATA_PTS = round(NUM_DATA_PTS / 2)

#all items to have data proccessed the same way
MEDIAN_CLEAN = ["motor", "gyroscope", "ultrasonic"]

#the distance to create a buffer zone around the entrance to prevent ever going back out the way we came in
ENTR_BUFFER_LEN = .1 #meters

ULTRA_THRESH = 30 # wall exists < 30 wall does not exist > 30


##GROVE INSTANCE
GROVE = grove

##LEGO INSTANCE
LEGO = bp.BrickPi3()

##BRICKPI INSTANCE
BP = bp

##ROBOT STRUCT
"""
    list of dicts, where each dict is a component of the robot ie a motor
    name: location_type (motor, ultrasonic, ir)
    port: take a wild guess
    wheel_dia: diameter of the wheel in meters
    inverse: if inverse then neg encoder reading is going in pos direction
"""
ROBOT = [
    {"name": "left_motor", "port": LEGO.PORT_A, "wheel_dia": WHEEL_DIA, "inverse": True},
    {"name": "right_motor", "port": LEGO.PORT_B, "wheel_dia": WHEEL_DIA, "inverse": True},
    {"name": "any_gyroscope", "port": LEGO.PORT_3, "sensor_type": LEGO.SENSOR_TYPE.EV3_GYRO_ABS},
    {"name": "left_ultrasonic", "port": 2},
    {"name": "front_ultrasonic", "port": 3},
    {"name": "right_ultrasonic", "port": 7},
]

