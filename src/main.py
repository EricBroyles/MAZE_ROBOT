import constants
import config

from robot import Robot



#stores the main logic to run at the final test day

try:
    myRobot = Robot()
    myRobot.initRobot()
    
except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    print("You pressed ctrl+C...")
