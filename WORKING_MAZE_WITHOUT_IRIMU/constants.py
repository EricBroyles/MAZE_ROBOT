import lib.brickpi3 as bp
import lib.grovepi as grove

##CONSTANTS
#Coordinate System
INIT_X_POS = 0
INIT_Y_POS = 0 

#the initial direction
POS_Y_VEC = (0, 1)

SPACE_CODE = 0
ORIGIN_CODE = 3
POINT_CODE = 1

#the size of the wheel in m

#2 5/16 = 2.3125 in = .0587 m
#2 4/16 = 2.25 in = .0572 m
#.056 m
#.055 m
#.0565 m
#.0568 m
WHEEL_DIA = .0587 #0.05665 #meters

LEFT_TURN_DPS = 120 #the dps the robot will atempt to turn at
RIGHT_TURN_DPS = 120

LEFT_MOVE_DPS = 180 #the dps the robot will atempt to travel at
RIGHT_MOVE_DPS = 180

SLOW_LEFT_MOVE_DPS = 120 #the dps the robot will atempt to travel at
SLOW_RIGHT_MOVE_DPS = 120

DUMP_DPS = 120 #the dps to dump items from robot

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
MEDIAN_CLEAN = ["motor", "gyroscope", "ultrasonic", "gate"]

TIME_TO_TURN_90 = 2.5 #s changes with dps
BEGIN_READING_AFTER = .75 #75% of the turn time is complete


#the distance to create a buffer zone around the entrance to prevent ever going back out the way we came in
ENTR_BUFFER_LEN = .1 #meters
WIDE_OPEN_ULTRA_THRESH = 80 #if ultra see more than this then seeing a cavern or the exit most likly
SPACE_ULTRA_THRESH = 36 # open space exists above 36 val read from ultrasonics
CONTACT_ULTRA_THRESH = 10 #about to come into contact with a wall
CENTER_THRESH = 40 #the abs of the degree that the robot couold at most turn away from the ideal orientation
X_JUNC_THRESH = .40#cm, the size of a hallwaythe area for a junction
Y_JUNC_THRESH = .40 #the size of a hallway and the area for a junction

NORM_ENCODERS_FUNC = [.00019697421409753857, -0.003258823003701462, .06827101159378236] #0.00019697421409753857 (log(x))^2 +  -0.003258823003701462 log(x) +  0.06827101159378236


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

##DO NOT USE PORT 2, it does not work!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ROBOT = [
    {"name": "left_motor", "port": LEGO.PORT_C, "wheel_dia": WHEEL_DIA, "inverse": True},
    {"name": "right_motor", "port": LEGO.PORT_A, "wheel_dia": WHEEL_DIA, "inverse": True},
    {"name": "back_gate", "port": LEGO.PORT_D, "inverse": True},
    {"name": "any_gyroscope", "port": LEGO.PORT_1, "sensor_type": LEGO.SENSOR_TYPE.EV3_GYRO_ABS},
    {"name": "left_ultrasonic", "port": 3},
    {"name": "front_ultrasonic", "port": 4},
    {"name": "right_ultrasonic", "port": 7},
]

