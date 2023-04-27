from constants import *
from config import configRobot, orientToYAxis
from actions import *
from helpers import *
from inputs import read
from navigate import *
from junctions import *
from update import *
from map import getMap
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

##CONFIG
configRobot()
kill = "removealltexttostoprunnawayrobot"

left_data = []
right_data = []

try:
    if kill != "":
        startMove()
        items = 50
        while(items > 0):
            norm_reading = read("ultrasonic")

            left_data.append(norm_reading["left_ultrasonic"])
            right_data.append(norm_reading["right_ultrasonic"])

            items -= 1
    stop()
    print(left_data)
    print(right_data)
    
    time = np.arange(len(left_data))

    title_font = {
        'family': 'normal',
        'weight': 'bold',
        'size': 22,
    }

    label_font = {
        'family': 'normal',
        'weight': 'bold',
        'size': 16,
    }

    # Plot the data
    plt.plot(time, left_data, 'b-', label='Left Ultrasonic (Junction)')
    plt.plot(time, right_data, 'r--', label='Right Ultrasonic')

    # Add title and labels
    plt.title('Ultrasonic Readings as Robot approaches Left Junction', fontdict=title_font)
    plt.xlabel('Time', fontdict=label_font)
    plt.ylabel('Ultrasonic Reading', fontdict=label_font)

    # Add legend
    plt.legend(prop={'size': 16, 'weight': 'bold'})

    # Show the plot
    plt.show()
    stop()

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    stop()
    print("You pressed ctrl+C...")

print("END -> RESET")
LEGO.reset_all()
