from time import time
import lib.brickpi3 as BP
import lib.grovepi as GROVE
from helpers import initSensorDelay


class Robot:

    def __init__(self):

        ##GROVE INSTANCE
        self.grove = GROVE

        ##LEGO INSTANCE
        LEGO = BP.BrickPi3()
        self.lego = LEGO

        ##ROBOT STRUCT
        """
            list of dicts, where each dict is a component of the robot ie a motor
            type: motor, ultrasonic, ir
            loc: location on robot ie front_left
            port: 
            wheel_dia: diameter of the wheel in meters
            init_delay: for select sensors that will read invalid if not given time to config
        """
        ROBOT = [
            {"type": "motor", "loc": "left", "port": LEGO.Port_A, "wheel_dia": 10, "init_delay": False},
            {"type": "motor", "loc": "right", "port": LEGO.Port_D, "wheel_dia": 10, "init_delay": False},
            {"type": "gyroscope", "loc": "any", "port": LEGO.Port_1, "sensor_type": LEGO.SENSOR_TYPE.EV3_GYRO_ABS, "init_delay": True},
            {"type": "ultrasonic", "loc": "left", "port": 4, "init_delay": False},
            {"type": "ultrasonic", "loc": "front", "port": 8, "init_delay": False},
            {"type": "ultrasonic", "loc": "right", "port": 7, "init_delay": False},
        ]

        ##TIME DATA
        """
            baseTime: gets set once to be used to find the elapsed time
            time: gets regularly updated with the current time
        """
        self.baseTime = time.time()
        self.time = self.baseTime

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
    

    """
    Actions:
    motor -> reset the motor encoder
    gyroscope -> set sensor type, perform delay until reading values

    """
    def initRobot(self):

        for item in self.ROBOT:
            if "motor" in item.keys():
                amount = self.lego.get_motor_encoder(item["port"])
                self.lego.offset_motor_encoder(item["port"], amount)
            elif "gyroscope" in item.keys():
                self.lego.set_sensor_type(item["port"], item["sensor_type"])

                ###NEED TO FINISH
                initSensorDelay()
        

    def updateTime(self):
        self.time = time.time()

    """
    returns the time that has passed from start in ms
    """
    def getTime(self):
        return (self.time - self.baseTime)

    def updatePosition(self):
        pass


    """
    generic function to read any sensor or encoder on the robot

    when loc is unspecified, and their are multiples of the same type all will be returned
    """
    def readData(type, loc = None):


    



        






