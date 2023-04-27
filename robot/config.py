import time
from constants import *
from helpers import getLocType
from actions import turn, resetEncoders

#waits for a LEGO sensor to be configured
#the lego instance, and the BP instance
def loadSensor(port):
    senseError = True
    runTime = 0
    while senseError and runTime <= MAX_SENSOR_CONFIG_TIME:
        try:
            value = LEGO.get_sensor(port)
            senseError = False
        except BP.SensorError as error:
            senseError = error
            print("Loading Sensor: ", error)

        runTime += DELAY
        time.sleep(DELAY)
    
    if senseError:
        print(f"ERROR [ Pre: @config ] loading sensor failed, check port and connection")

    else:
        print(f"SUCCESS [ Pre: @config ] loading sensor complete")

##configures any robot item, motors, gyro, ultra
def configRobot():
    
    for item in ROBOT:
        loc, type = getLocType(item)

        if(type == "motor"):
            LEGO.reset_motor_encoder(item["port"])
            print(f"[ Pre: @config ] {item['name']} reset to 0 -> {LEGO.get_motor_encoder(item['port'])}")
        
        elif(type == "gate"):
            LEGO.reset_motor_encoder(item["port"])
            print(f"[ Pre: @config ] {item['name']} reset to 0 -> {LEGO.get_motor_encoder(item['port'])}")

        elif(type == "gyroscope"):
            LEGO.set_sensor_type(item['port'], item['sensor_type'])
            loadSensor(item["port"])
            print(f"[ Pre: @config ] {item['name']} reading valid -> {LEGO.get_sensor(item['port'])}")

        elif(type == "ultrasonic"):
            print(f"[ Pre: @config ] {item['name']} reading valid -> {GROVE.ultrasonicRead(item['port'])}")

        elif(type == "magnet"):
            print(f"[ Pre: @config ] {item['name']} reading valid -> {MPU.readMagnet()}")

        elif(type == "ir"):
            try:
                print(f"[ Pre: @config ] {item['name']} reading valid -> {GROVE.analogRead(item['port'])}")
            except IOError as error:
                print(error)
        else:
            try:
                print(f"ERROR [ Pre: @config ] item type: {item['type']} does not match any know type")
            except IOError as error:
                print(error)

    print("@config: COMPLETE CONFIG")

def orientToYAxis():
    ans = input("CHECK: DID I PLACE THE ROBOT FACING THE X-AXIS (y/n) ")
    if(ans != "y"):
        input("PLEASE HIT ctrl-c to restart")
    else:
        turn(90)
    resetEncoders()
    print("ROBOT IS FACING THE y-axis")