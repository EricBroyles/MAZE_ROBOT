name = "magnet11"
print(name[:6])

# points = [[0, 0], [0, 1], [0, 2], [3, 2]]



# def findIndex(target, points_matrix):
#     for r, row in enumerate(points_matrix):
#         for c, col in enumerate(row):
#             if col['pt'] is not None and round(col['pt'], 4) == round(target, 4):
#                 return r, c
#     return None

# def makeLines(points, points_matrix):

#     for i_p, pt in enumerate(points):
#         if i_p > 0:
#             prev_row, prev_col = findIndex(points[i_p - 1], points_matrix)
#             row, col = findIndex(pt, points_matrix)

#             row_inc = 1 if row > prev_row else -1
#             col_inc = 1 if col > prev_col else -1

#             for row in range(prev_row, row + row_inc, row_inc):
#                 for col in range(prev_col, col + col_inc, col_inc):
#                     if points_matrix[row][col]["tag"] == 0:
#                         points_matrix[row][col]["tag"] = 1
    
# def addPoints(points, bounds_matrix):

#     result_matrix = []

#     for row in bounds_matrix:
#         result_row = []
#         for bounds in row:
#             new_bounds = bounds.copy()
#             for i, point in enumerate(points):
#                 if bounds['x'][0] <= point[0] <= bounds['x'][1] and bounds['y'][0] <= point[1] <= bounds['y'][1]:
#                     if point[0] == 0 and point[1] == 0:
#                         new_bounds['tag'] = 5 #origin
#                     elif i == len(points) - 1:
#                         new_bounds['tag'] = 4 #exit
#                     else:
#                         new_bounds['tag'] = 1 #path
#                     new_bounds['pt'] = point

#             result_row.append(new_bounds)
#         result_matrix.append(result_row)

#     return result_matrix

# #last step
# def addHazards(hazards, lines_matrix):
#     for r, row in enumerate(lines_matrix):
#         for c, bounds in enumerate(row):
#             for name, pt in hazards.items():
#                 if bounds['x'][0] <= pt[0] <= bounds['x'][1] and bounds['y'][0] <= pt[1] <= bounds['y'][1]:
#                     if name == "heat":
#                         tag = 2
#                     elif name == "magnetic":
#                         tag = 3
#                     #only override pah info and non path info
#                     if lines_matrix[r][c]['tag'] <= 1:
#                         lines_matrix[r][c]['tag'] = tag

# def simplifyMatrix(lines_hazards_matrix):
#     csv_ready = []
#     for r, row in enumerate(lines_hazards_matrix):
#         li = []
#         for c, col in enumerate(row):
#             li.append(lines_hazards_matrix[r][c]['tag'])

#         csv_ready.append(li)
#     return csv_ready


# def getBoundsMatrix(pts, grid_size = .40):

#     #create the map matrix
#     max_x = round(max(point[0] for point in pts), 1)
#     min_x = round(min(point[0] for point in pts), 1)
#     max_y = round(max(point[1] for point in pts), 1)
#     min_y = round(min(point[1] for point in pts), 1)
#     floatify = .0000001
#     y_ranges = []
#     y = max_y + grid_size / 2
#     while y >= min_y - grid_size:
#         y_ranges.append(y)
#         y -= grid_size 

#     x_ranges = []
#     x = min_x - grid_size / 2
#     while x <= max_x + grid_size:
#         x_ranges.append(x)
#         x += grid_size 
    
#     matrix = []
#     for r, row_range in enumerate(y_ranges):
#         if r > 0:
#             l = []
#             for c, col_range in enumerate(x_ranges):
#                 if c > 0:
#                     x_bounds = [round(x_ranges[c-1], 8), round(col_range - floatify, 8)]
#                     y_bounds = [round(row_range, 8), round(y_ranges[r-1] - floatify, 8)]
#                     bounds = {"x": x_bounds, "y": y_bounds, "tag":0, "pt": None}
#                     l.append(bounds)
#             matrix.append(l)
#     return matrix

# #when adding hazards convert the array of tuples into an array of []
# matrix = getBoundsMatrix(points)
# # for r in matrix:
# #     print(r)
# with_pts = addPoints(points, matrix)


# makeLines(points, with_pts)

# for r in with_pts:
#     print(r)
#     print()


# # import math
# # # def move(distance):

# # #     #distance = abs(distance)

# # #     #motor_reading = read("motor") #get the most accurate reading
# # #     #(left_motor, right_motor) = (motor_reading["left_motor"], motor_reading["right_motor"])
# # #     final_encoder_val = 360 * (abs(distance) / (pi * WHEEL_DIA)) + (abs(right_motor) + abs(left_motor)) / 2
# # #     # if distance > 0:
# # #     #     startMove(LEFT_MOVE_DPS, RIGHT_MOVE_DPS)
# # #     # elif distance < 0:
# # #     #     startMove(-SLOW_LEFT_MOVE_DPS, -SLOW_RIGHT_MOVE_DPS)

# # #     while((abs(right_motor) + abs(left_motor)) / 2 <= final_encoder_val):
# # #         #time.sleep(DELAY)
# # #         motor_reading = fastRead("motor")
# # #         (left_motor, right_motor) = (motor_reading["left_motor"], motor_reading["right_motor"])

# # #     print(f"@move: complete -> (left: ", read("motor")["left_motor"], ", right: " , read("motor")["right_motor"], ")")

# # #     #print("@MOVE: DONE MOVE -> LEFT: ", read("motor")["left_motor"]  , " RIGHT: ", read("motor")["right_motor"], " vs: ", final_encoder_val )
    
# # #     stop()

# # distance = 1
# # right_motor = 360
# # left_motor = 360
# # final_encoder_val = 360 * ((distance) / (math.pi * 1/ math.pi)) + ((right_motor) + (left_motor)) / 2
# # print(final_encoder_val)


# # # def createConnections(prev_junc_id, new_back_junc_item, junc_items):
# # #     """
# # #     @prev_junc_id: int -> the id the robot was in before the current junc
# # #     @new_back_junc_item: {junc_item} -> a back arrow for the junction currently in
# # #     @junc_items: [{junc_item}, ...]

# # #     updates is_connect for at most two junc_items, the new_back_arrow and what it is connected to

# # #     """
# # #     curr_junc_id = new_back_junc_item["id"]
# # #     back_x, back_y = new_back_junc_item["dir_vec"]


# # #     for junc in (junc_items):
# # #         if junc["id"] == prev_junc_id and not junc["is_back"]:
# # #             x, y = junc["dir_vec"]
# # #             if -x == back_x and -y == back_y:
# # #                 #it is connected
# # #                 junc["connect_id"] = curr_junc_id
# # #                 break

# # #     for junc in junc_items:
# # #         if junc["id"] == curr_junc_id:
# # #             junc["connect_id"] = prev_junc_id
# # #             break

# # # junc_items = [
# # #     {"id": 1, "connect_id": None, "is_expl": True, "pos": (1, 1), "dir_vec": (0, 1), "is_back": False},
# # #     {"id": 1, "connect_id": None, "is_expl": True, "pos": (1, 1), "dir_vec": (0, -1), "is_back": True},
# # #     {"id": 2, "connect_id": None, "is_expl": True, "pos": (2, 2), "dir_vec": (0, 1), "is_back": False},
# # #     {"id": 2, "connect_id": None, "is_expl": True, "pos": (2, 2), "dir_vec": (-1, 0), "is_back": False},
# # #     {"id": 2, "connect_id": None, "is_expl": True, "pos": (2, 1), "dir_vec": (0, -1), "is_back": True},
# # # ]

# # # prev_junc_id = 1
# # # new_back_junc_item = {"id": 2, "connect_id": None, "is_expl": True, "pos": (2, 1), "dir_vec": (0, -1), "is_back": True}

# # # createConnections(prev_junc_id, new_back_junc_item, junc_items)

# # # for item in junc_items:
# # #     print(item)