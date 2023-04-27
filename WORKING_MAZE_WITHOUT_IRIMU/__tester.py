##all the old used tests that are not needed anymore

##WARNING: CHECK CODE, it will change
##all items should be considered to be reference only

"""

if test == "time_to_turn":
        for deg in range(90, 360, 90):
            t = time.time()
            turn(deg)
            print(time.time() - t)
            print(read("gyroscope"))
            pause()

        stop()

    if test == "run_experiment":
        runExperiment("distance_vs_error")

    if test == "encoderval_to_distance":
        left_motor, right_motor = (0,0)
        startMove()
        while abs(left_motor + right_motor) / 2 <= 3800:
            reading = read("motor")
            right_motor = reading['right_motor']
            left_motor = reading['left_motor']
        stop()

    if test == "hallway_center":
        orientToYAxis()
        ideal_dir_vec = (0,1)
        all_sensors_data = []
        found_exit = False

        startMove()

        while(not found_exit):
            sensors = read()
            print(sensors)
            all_sensors_data.append(sensors)
            center(sensors, ideal_dir_vec)
            is_junc, is_deadend, is_exit, is_hallway = checkSenarios(all_sensors_data[-1])
            found_exit = is_exit

        stop()
        print("hallway complete")
    

    if test == "move":
        move(.305)
        pause()
        move(.305)
        pause()
        move(.305)
        pause()
        move(.305)
        stop()
        print(read())
    if test == "far_move":
        move(.305 * 4)
        pause()
        move(.305 * 2)
        pause()
        move(.305 * 2)
        pause()
        move(.305 * 2)
        stop()
        print(read())
    if test == "turn":
        turn(90 * 2)
        print("gyro reads: ", read("gyroscope"))
        pause()
        turn(-90 * 2)
        print("gyro reads: ", read("gyroscope"))
        pause()
        turn(90 *2)
        print("gyro reads: ", read("gyroscope"))
        pause()
        turn(-90 *2)
        print("gyro reads: ", read("gyroscope"))
        stop()
    if test == "read":
        while(True):
            print(read())
            time.sleep(.01)
    if test == "read_gyro":
        while(True):
            print(read("gyroscope"))
            time.sleep(.01)

    if test == "read_ultra":
        while(True):
            print(read("ultrasonic"))
            time.sleep(.01)

    if test == "encoder_dist":

        ##BADD CODE REFERENCE ONLY
        startMove()
        num = 25
        while(num > 0):
            print(read("motor")['right_motor'] , " vs ",  read("motor")['left_motor'])
            num -= 1
        print("FINAL")
        right_motor = read("motor")['right_motor']
        left_motor = read("motor")['left_motor']
        encoder_reading_final = (right_motor + left_motor) / 2
        print("ENCODERS: ", right_motor , " vs ",  left_motor, " vs ", encoder_reading_final)
        c = WHEEL_DIA * math.pi
        rev = encoder_reading_final / 360
        distance_traveled_meters = c * rev
        distance_traveled_inches = distance_traveled_meters * 39.37
        print("Distance traveled: {:.2f} meters, {:.2f} inches".format(distance_traveled_meters, distance_traveled_inches))

        stop()
    if test == "encoder_diff":
        startMove()
        num = 100
        while(num > 0):
            print(num, " === ", read("motor")['right_motor'] - read("motor")['left_motor'])
            num -= 1
        stop()

    if test == "ultrasonic_bounds":
        while(True):
            print(read("ultrasonic"))

"""