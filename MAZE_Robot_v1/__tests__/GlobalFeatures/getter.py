from main import myRobot

def getInfo():
    myRobot.updatePosition()
    print("getter", myRobot.position)