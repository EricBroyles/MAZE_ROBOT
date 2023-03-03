import time
from constants import BP, LEGO, GROVE, LEGO_ITEMS, DELAY

##configures any item for, motors, gyro
def configLEGO():

    for item, port in LEGO_ITEMS.items():
        
        if(item[0:5] == "MOTOR"):
            currEncoder = LEGO.get_motor_encoder(port)
            LEGO.offset_motor_encoder(port, currEncoder)

            print("@config: ", item, " encoder =  ", LEGO.get_motor_encoder(port), " -> should be 0")

        elif(item == "EV3_GYRO"):
            LEGO.set_sensor_type(port, LEGO.SENSOR_TYPE.EV3_GYRO_ABS)

            senseError = True
            while senseError:
                
                try:
                    value = LEGO.get_sensor(port)
                    senseError = False
                except BP.SensorError as error:
                    senseError = error
                    print("ERROR: ", error)
                
                time.sleep(DELAY)

            print("@config: ", item, " sensor =  ", LEGO.get_sensor(port), " -> should be not invalid")
            
        else:
            print("@config ERROR !!!!!!! Invalid item -> check spelling in @config and @constants ")
