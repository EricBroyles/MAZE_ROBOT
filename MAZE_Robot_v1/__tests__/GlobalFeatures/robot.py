class Robot:
    def __init__(self, time = 0, position = 0):
        self.time = 0
        self.position = 0

    def updateTime(self):
        self.time += 1

    def updatePosition(self):
        self.position += 1