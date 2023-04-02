
import time
from constants import *
from config import configRobot


##CONFIG
configRobot()


try:

    found_exit = False

    while not(found_exit):
        #explore


        pass
    pass

    #create graph

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    print("You pressed ctrl+C...")