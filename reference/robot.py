from time import time
from constants import *
from config import configRobot
import lib.brickpi3 as BP
import lib.grovepi as GROVE
from inputs import read


class Robot:
    def __init__(self):

        ##GROVE INSTANCE
        self.grove = GROVE

        ##LEGO INSTANCE
        LEGO = BP.BrickPi3()
        self.brick = BP
        self.lego = LEGO

        ##ROBOT STRUCT
        """
            list of dicts, where each dict is a component of the robot ie a motor
            type: motor, ultrasonic, ir
            loc: location on robot ie front_left
            port: take a wild guess
            wheel_dia: diameter of the wheel in meters
            inverse: if inverse then neg encoder reading is going in pos direction
        """
        ROBOT = [
            {"type": "motor", "loc": "left", "port": LEGO.Port_A, "wheel_dia": WHEEL_DIA, "inverse": True},
            {"type": "motor", "loc": "right", "port": LEGO.Port_D, "wheel_dia": WHEEL_DIA, "inverse": True},
            {"type": "gyroscope", "loc": "any", "port": LEGO.Port_1, "sensor_type": LEGO.SENSOR_TYPE.EV3_GYRO_ABS},
            {"type": "ultrasonic", "loc": "left", "port": 4},
            {"type": "ultrasonic", "loc": "front", "port": 8},
            {"type": "ultrasonic", "loc": "right", "port": 7},
        ]

        ##TIME DATA
        """
            baseTime: gets set once to be used to find the elapsed time
            time: gets regularly updated with the current time
        """
        self.baseTime = None
        self.time = None

        ##POSITION DATA
        """
            array of dict holding time based position data
            ex: [{"t": 1551143536.9323719, "x": 0, "y": 0}, etc...]
        """
        self.position = []

        ##MOTOR POSITION DATA (ENCODERS)
        """
            stores the current reading for each of the encoders, derives itself from the motors setup in constants
            ex: {"motor_front_left": 0, "motor_front_right": 0, "motor_back_left": 0, "motor_back_right": 0}
        """
        self.motorPositions = {}

        ##SENSOR DATA
        """
            stores the current reading for each of the sensors, derived from the constants
            IR, ultrasonic, etc
            ex: {"ultrasonic_left": 0, "ultrasonic_right": 0, "ultrasonic_front": 0, "ir_front": 0}
        """
        self.sensors = {}
        
    def __str__(self):
        return f"myRobot -> {self.time - self.baseTime}: "
    
    def initRobot(self):
        """
        initialize all sensors, wait for them to be configured
        set all encoder to 0
        configure time and space
        """
        configRobot()

        #config space and time
        self.baseTime = time.time()
        self.time = self.baseTime
        self.position = [{"t": self.baseTime, "x": INIT_X_POS, "y": INIT_Y_POS}]

    def updateTime(self):
        self.time = time.time()

    def getTime(self):
        """
        returns the time that has passed from start in s
        """
        return (self.time - self.baseTime)

    def setPosition(self, pos):
        """
        pos = the accurate position of the robot at some time instance
        """
        self.position = self.position.append(pos)
        

    def readData(self, type, loc = None):
        """
        gen function to read any sensor or encoder on the robot

        when loc is unspecified, and their are multiples of the same type all will be returned
        """

        #get the items
        items = []
        for item in self.ROBOT:
            if(item["type"] == type):
               if(loc == None or loc == item["loc"]):
                   items.append(item)

        return read(items, type)




    



        






