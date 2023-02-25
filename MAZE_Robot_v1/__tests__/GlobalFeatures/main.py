from robot import Robot
import other


print("running main")
myRobot = Robot()

from getter import getInfo

myRobot.updatePosition()

print("main",myRobot.position)

getInfo()

