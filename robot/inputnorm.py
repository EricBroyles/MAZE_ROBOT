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

raw_data = []
norm_data = []

try:
    if kill != "":
        items = 100
        while(items > 0):
            reading = GROVE.ultrasonicRead(4)
            raw_data.append(reading)
            norm_reading = read("ultrasonic")["front_ultrasonic"]
            norm_data.append(norm_reading)
            items -= 1
            print(reading, " vs ", norm_reading)

    
    time = np.arange(len(raw_data))

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
    plt.plot(time, raw_data, 'b--', label='Raw Data')
    plt.plot(time, norm_data, 'k-', label='Normalized Data')

    # Add title and labels
    plt.title('Ultrasonic Readings in Open Space', fontdict=title_font)
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
