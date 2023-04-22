
# add the positon data first, without destroying the bouding infor
#then fill in the path lines with the above data

#then add any hazards overriding position data if neccisary
#upload this raw_map to csv
#then upload map to csv with just the 1, 2,3 info

from constants import *

#points is [[x,y], ...]
def getBoundsMatrix(pts, grid_size = .40):

    #create the map matrix
    max_x = round(max(point[0] for point in pts), 1)
    min_x = round(min(point[0] for point in pts), 1)
    max_y = round(max(point[1] for point in pts), 1)
    min_y = round(min(point[1] for point in pts), 1)

    y_ranges = []
    y = max_y + grid_size / 2
    while y >= min_y - grid_size:
        y_ranges.append(round(y,2))
        y -= grid_size

    x_ranges = []
    x = min_x - grid_size / 2
    while x <= max_x + grid_size:
        x_ranges.append(round(x, 2))
        x += grid_size
    
    matrix = []
    for r, row_range in enumerate(y_ranges):
        if r > 0:
            l = []
            for c, col_range in enumerate(x_ranges):
                if c > 0:
                    x_bounds = [x_ranges[c-1], col_range]
                    y_bounds = [row_range, y_ranges[r-1]]
                    bounds = [x_bounds, y_bounds]
                    l.append(bounds)
            matrix.append(l)
    return matrix

# def replace(points, matrix):

#     pts_left = [row.copy() for row in points]
#     new_matrix = [row.copy() for row in matrix]

    
#     for row in range(0, len(matrix)):
#         for col in range(0, len(matrix[0])):
#             for pt in pts_left:
#                 x = pt[0]
#                 y = pt[1]
#                 x_bounds, y_bounds = matrix[row][col]

#                 if x >= x_bounds[0] and x <= x_bounds[1]:
#                     if y >= y_bounds[0] and y <= y_bounds[1]:
#                         if x == 0 and y == 0:
#                             new_matrix[row][col] = 3
#                         else: 
#                             new_matrix[row][col] = 3
#     return new_matrix

def addPointData(points, matrix):
    new_matrix = [row.copy() for row in matrix]

    for pt in points:
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                item = matrix[r][c]
                if len(item) < 3:
                    x = pt[0]
                    y = pt[1]
                    x_low, x_high = (item[0][0], item[0][1])
                    y_low, y_high = (item[1][0], item[1][1])

                    if x >= x_low and x <= x_high:
                        if y >= y_low and y <= y_high:
                            if x == 0 and y == 0:
                                new_matrix[r][c].append(ORIGIN_CODE)
                            else: 
                                new_matrix[r][c].append(POINT_CODE)

    return new_matrix

def makeLines(matrix):
    new_matrix = [row.copy() for row in matrix]

    

    return new_matrix




#[(x,y), ...], floats are allowed
#units are in meters
#grid size is defined by .40, .40
def getMap(points):
    #convert points into array of arrays [[x,y], ...] round all items to 2 decimal places
    pts = [[round(tup[0], 2), round(tup[1], 2)] for tup in points]

    matrix = getBoundsMatrix(pts)

    print("bounds matrix")
    for row in matrix:
        print(row)

    matrix = addPointData(points, matrix)

    matrix = makeLines(matrix)
    return matrix




