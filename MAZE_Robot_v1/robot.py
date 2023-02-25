from time import time


##all constants infor about the robot, ie port nums, and diameters of wheels is stored in constants

##any info about the motor stored here should be dynamic ie the current encoder reading

class Robot:


 #will also store the 
    #initializ basic info about the robot
    #wheels -> name, motor: {port}
    #need wheel diameter
    #need motor info: name, should it be inversed, port, wheel diameter

    ##need to store the encoder reading, the reading from any sensors


    def __init__(self):

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
        return f""

    def updateTime(self):
        self.time += 1

    def updatePosition(self):
        self.position += 1



        

##ROBOT STRUCT
"""
    list of dicts, where each dict is a component of the robot ie a motor

    {"motor_front_left": 0, "motor_front_right": 0, "motor_back_left": 0, "motor_back_right": 0}
"""
ROBOT = [
    {"name": "motor_front_left", "type": "motor", "location": "front_left", "port": "", "init_type": None, "pin_mode": None, "data_type": },
]



