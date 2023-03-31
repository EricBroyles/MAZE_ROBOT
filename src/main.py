
import time
from constants import *
from config import configRobot


##CONFIG
configRobot()


        #config space and time
        self.baseTime = time.time()
        self.time = self.baseTime
        self.position = [{"t": self.baseTime, "x": INIT_X_POS, "y": INIT_Y_POS}]

try:

    found_exit = False

    while not(found_exit):



        pass
    pass

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    print("You pressed ctrl+C...")
