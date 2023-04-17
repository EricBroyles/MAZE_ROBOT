import math
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import polynomial as P
print("comment actions out if not running on pi")
from actions import *

#run experiments to collect data to be normalized
def runTrialItem(num_ticks):
    run = True
    while run:
        print("\n====================================================================")
        ans = input("1. INSTRUCTIONS: set the robot at 0 in, enter anything to cont.... ")
        print("====================================================================\n")
        
        resetEncoders()
        reading = read("motor")
        left_motor, right_motor = (reading['left_motor'], reading['right_motor'])
        print("RESET encoders (left: ", left_motor, ", right: ",right_motor, ")")
        
        startMove()
        while(abs(left_motor + right_motor) / 2 < num_ticks):
            reading = read("motor")
            left_motor, right_motor = (reading['left_motor'], reading['right_motor'])
            read("motor")

        stop()

        print("EXPERIMENT trial complete (left: ", left_motor, ", right: ", right_motor, ")")
        print("\n====================================================================")
        actual_distance = input("2. INSTRUCTIONS: input the actual distance (inches) (null or n to redo trial): ")
        print("====================================================================\n")

        if actual_distance.lower() != "null" and actual_distance.lower() != "n":
            run = False
            actual_distance = float(actual_distance)
            print("EXPERIMENT you entered: ", actual_distance)
        else:
            print("!! ISSUE !! entered (", actual_distance, ") repeating trial")
            
    return left_motor, right_motor, actual_distance

#trial_vals = {"left_motor": [row of data], "right_motor": [row of data] ,"actual_distance": [row of data]}
#csv_names = ["left_motor, "right_motor", "actual_distance"], correspond to the names of files to add the appropriate trial_vals to
def storeRowData(trial_vals, csv_names):
    
    for name in csv_names:
        with open(name + ".csv", mode='a', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(trial_vals[name])
    
def collectData(num_trials, encoder_ticks, csv_names):

    total_items = num_trials * len(encoder_ticks)
    items_left = total_items

    for trial in range(0, num_trials):

        left_motor_trial = []
        right_motor_trial = []
        actual_distance_trial = []

        for num_ticks in encoder_ticks:

            left_motor, right_motor, actual_distance = runTrialItem(num_ticks)
            left_motor_trial.append(left_motor)
            right_motor_trial.append(right_motor)
            actual_distance_trial.append(actual_distance)

            items_left -= 1
            print("EXPERIMENT ", items_left, " items left of ", total_items)

        print("STORING trial data")
        storeRowData({"left_motor": left_motor_trial, "right_motor": right_motor_trial ,"actual_distance": actual_distance_trial}, csv_names)

        print("EXPERIMENT trial ", trial + 1, " of ", num_trials, " complete")

        
def createCSVFiles(headers, csv_names):
    stopped = False

    for name in csv_names:
        if os.path.isfile(name + ".csv"):
            user_input = input(f"The file {name}.csv already exists. Do you want to override? (y/n) ")
            if user_input.lower() != 'y':
                stopped = True
                break
        with open(name + ".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            file.close()

    return stopped

def readCSVFile(file_name):
    # Load data from CSV file into a numpy array
    data = np.loadtxt(file_name, delimiter=",", skiprows=1)
    return data

def averageArrays(arr1, arr2):
    # Check that both arrays are the same size
    if arr1.shape != arr2.shape:
        raise ValueError("Input arrays must be of the same size")
    
    # Compute the average of the two arrays
    avg_arr = (arr1 + arr2) / 2
    
    return avg_arr

def graphCSVData(filename):
    x = []
    y = []
    z = []

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)

        for i, row in enumerate(reader):
            if i == 0:
                x = list(map(float, row[1:]))
            else:
                y.append(float(row[0]))
                z.append(list(map(float, row[1:])))

    # Create 3D surface plot
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    X, Y = np.meshgrid(x, y)
    ax.scatter3D(X, Y, z)
    #ax.contour3D(X, Y, Z, 50, cmap='binary')

    ax.set_xlabel("encoder ticks")
    ax.set_ylabel("wheel dia")
    ax.set_zlabel("error")
    ax.set_title(filename)

    plt.show()

def read_first_row_and_col(file_name):
    with open(file_name, 'r') as csvfile:
        # Create a CSV reader object
        csvreader = csv.reader(csvfile)
        
        # Get the first row of the CSV file
        row = next(csvreader)
        
        # Convert the row to a Python list and exclude the first column
        row_array = row[1:]
        
        # Get the first column of the CSV file
        col_array = [row[0] for row in csvreader]

        return row_array, col_array

# def createLinRegEq():

def graphMinCSVData(filename):
    x = [] #best_encoder _ticks
    y = [] #wheel_dia to achieve this

    data = readCSVFile(filename)
    data = np.delete(data, 0, axis = 1)

    encoder_ticks, test_wheel_dia = read_first_row_and_col(filename)

    col_min = [] #recoreded to veriry col_mins are correct
    row = None

    for col in range(len(data[0])):

        curr_col_min = data[0][col]

        for r in range(1, len(data)):
            val = data[r][col]
            if(abs(val) < abs(curr_col_min)):
                curr_col_min = val
                row = r

        x.append(float(encoder_ticks[col]))
        y.append(float(test_wheel_dia[row]))
        

        col_min.append(curr_col_min)

    print("col_min: ", col_min)
    print("x: ", x)
    print("y: ", y)

    #perform a polyfit

    log_fit = np.polyfit(np.log(x), y, 1)
    print("log_fit: ", log_fit)
    print("y = ", log_fit[0], "log(x) + ", log_fit[1])

    log_fit2 = np.polyfit(np.log(x), y, 2)

    poly_fit_1 = np.polyfit(x, y, 1)
    print("poly_fit_1: ", poly_fit_1)
    print()

    

    x_hat = np.linspace(300, max(x), 1000)
    log_y_hat = [log_fit[0] * np.log(n) + log_fit[1] for n in x_hat]

    log2_y_hat = []

    for n in x_hat:
        func_sum = 0
        for i, coef in enumerate(log_fit2):
            func_sum += coef * np.log(n)**(len(log_fit2) - (i+1))

        log2_y_hat.append(func_sum)

    poly1_y_hat = []

    for n in x_hat:
        func_sum = 0
        for i, coef in enumerate(poly_fit_1):
            func_sum += coef * n**(len(poly_fit_1) - (i+1))

        poly1_y_hat.append(func_sum)


    # Plot the data
    fig, ax = plt.subplots()
    ax.plot(x, y, 'o', label='encoder ticks vs wheel dia')
    ax.plot(x_hat, log_y_hat, '--', color = 'green', label='1st degree log')
    ax.plot(x_hat, log2_y_hat, color = 'black', label='2nd degree log')
    ax.plot(x_hat, poly1_y_hat, '-.', color = 'red', label = 'linear')
    
    ax.plot()
    ax.set_xlabel('Encoder Ticks')
    ax.set_ylabel('Test Wheel Diameter')
    ax.set_title(f'Finding ideal values for wheel dia vs encoder ticks for {filename}')

    plt.legend(loc='upper right')
    plt.gca().get_legend().legendHandles[0]
    plt.gca().get_legend().legendHandles[1]
    plt.gca().get_legend().legendHandles[2]
    plt.gca().get_legend().legendHandles[3]
    plt.show()





def runAnalysis():
    print("CHECK THAT YOU ARE IN THE CORRECT FILE PATH")
    analysis_names = ["sum", "average"]
    headers = ["wheel_dia"]
    test_wheel_dia = [x / 100000 for x in range(int(.06 * 100000),int( .05 * 100000), int(-.00001 * 100000))] #[.0587, .0572, .0569, .0567,.0562, .0557, .0552, .0547, .0542]

    right_motor_data = readCSVFile("right_motor.csv")
    left_motor_data = readCSVFile("left_motor.csv")
    actual_distance_data = readCSVFile("actual_distance.csv")

    final_encoder_data = np.absolute(averageArrays(right_motor_data, left_motor_data))

    print("final_encoder_data")
    print(final_encoder_data)

    print("averages")
    print(np.mean(final_encoder_data, axis=0).tolist())

    print("POSSIBLE ISSUE with numpy adding to list if error occurs here")
    stopped = createCSVFiles(headers + np.mean(final_encoder_data, axis=0).tolist(), analysis_names)
    if stopped:
        return

    for dia in test_wheel_dia:
        c = dia * math.pi

        encoder_distance_data = final_encoder_data / 360 * c * 39.37
        error = encoder_distance_data - actual_distance_data

        ##TWO DIFFERENT MODELS

        ##using sum will encourage the model to find items that straddle 0 error, ie over and undershoot equally
        error_sums = np.sum(error, axis=0)

        ##error averages, just looks for the model that can produce the smallest average error
        error_avg = np.mean(error, axis=0)

        storeRowData({"sum": np.insert(error_sums, 0, dia), "average": np.insert(error_avg, 0, dia)}, analysis_names)


def runExperiment(name):

    if name == "distance_vs_error":
        num_trials = 6
        encoder_ticks = list(range(600, 3600 + 600, 600))
        csv_names = ["left_motor", "right_motor", "actual_distance"]

        stopped = createCSVFiles(encoder_ticks, csv_names)

        if stopped:
            return

        collectData(num_trials, encoder_ticks, csv_names) #stores data into csv files

        runAnalysis()
        