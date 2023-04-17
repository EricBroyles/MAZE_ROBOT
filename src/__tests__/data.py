test_sensor_data = [
    {"front_ultrasonic": 80, "right_ultrasonic": 30, "left_ultrasonic": 30, "left_motor": 0, "right_motor": 0, "any_gyroscope": 90}, #start reading, in hallway
    {"front_ultrasonic": 80, "right_ultrasonic": 30, "left_ultrasonic": 30, "left_motor": 360, "right_motor": 360, "any_gyroscope": 90},
    {"front_ultrasonic": 80, "right_ultrasonic": 30, "left_ultrasonic": 30, "left_motor": 720, "right_motor": 720, "any_gyroscope": 90}, #last hallway section
    {"front_ultrasonic": 80, "right_ultrasonic": 80, "left_ultrasonic": 30, "left_motor": 1080, "right_motor": 1080, "any_gyroscope": 90}, #junction with right and front, continue forward
    {"front_ultrasonic": 80, "right_ultrasonic": 30, "left_ultrasonic": 30, "left_motor": 1440, "right_motor": 1440, "any_gyroscope": 90},
    {"front_ultrasonic": 30, "right_ultrasonic": 80, "left_ultrasonic": 80, "left_motor": 1800, "right_motor": 1800, "any_gyroscope": 90}, #two way junction
    {"front_ultrasonic": 30, "right_ultrasonic": 30, "left_ultrasonic": 30, "left_motor": 2160, "right_motor": 2160, "any_gyroscope": 0}, #hit dead end, navigate back
    {"front_ultrasonic": 80, "right_ultrasonic": 80, "left_ultrasonic": 30, "left_motor": 2520, "right_motor": 2520, "any_gyroscope": 180}, #find teh junc again, should not create the same junc
    {"front_ultrasonic": 80, "right_ultrasonic": 80, "left_ultrasonic": 80, "left_motor": 2880, "right_motor": 2880, "any_gyroscope": 180}, #find the exit
]