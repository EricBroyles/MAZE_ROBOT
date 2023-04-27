import csv

def findIndex(target, points_matrix):
    for r, row in enumerate(points_matrix):
        for c, col in enumerate(row):

            if col['pts'] is not None:
                pts = [[round(a, 4) for a in pt] for pt in col['pts']]
                targ = [round(x, 4) for x in target]
                if targ in pts:
                    return r, c
    return None

def makeLines(points, points_matrix):

    for i_p, pt in enumerate(points):
        
        if i_p > 0:
            prev_row, prev_col = findIndex(points[i_p - 1], points_matrix)
            row, col = findIndex(pt, points_matrix)

            row_inc = 1 if row > prev_row else -1
            col_inc = 1 if col > prev_col else -1

            for row in range(prev_row, row + row_inc, row_inc):
                for col in range(prev_col, col + col_inc, col_inc):
                    if points_matrix[row][col]["tag"] == 0:
                        points_matrix[row][col]["tag"] = 1
    
def addPoints(points, bounds_matrix):

    result_matrix = []

    for row in bounds_matrix:
        result_row = []
        for bounds in row:
            new_bounds = bounds.copy()
            for i, point in enumerate(points):
                if bounds['x'][0] <= point[0] <= bounds['x'][1] and bounds['y'][0] <= point[1] <= bounds['y'][1]:

                    if new_bounds['pts'] is None:
                        new_bounds['pts'] = []

                    if point[0] == 0 and point[1] == 0:
                        new_bounds['tag'] = 5 #origin
                    elif i == len(points) - 1:
                        new_bounds['tag'] = 4 #exit
                        
                    elif new_bounds['tag'] == 0:
                        new_bounds['tag'] = 1 #path

                    new_bounds['pts'].append(point)

            result_row.append(new_bounds)
        result_matrix.append(result_row)

    return result_matrix

#last step
def addHazards(hazards, lines_matrix):
    for r, row in enumerate(lines_matrix):
        for c, bounds in enumerate(row):
            for name, pt in hazards.items():
                if bounds['x'][0] <= pt[0] <= bounds['x'][1] and bounds['y'][0] <= pt[1] <= bounds['y'][1]:
                    #allows names like heat1, or magnet12, etc
                    tag = 0
                    if name[:4] == "heat":
                        tag = 2
                    elif name[:6] == "magnet":
                        tag = 3
                    #only override pah info and non path info
                    if lines_matrix[r][c]['tag'] <= 1:
                        lines_matrix[r][c]['tag'] = tag

def simplifyMatrix(lines_hazards_matrix):
    csv_ready = []
    for r, row in enumerate(lines_hazards_matrix):
        li = []
        for c, col in enumerate(row):
            li.append(lines_hazards_matrix[r][c]['tag'])

        csv_ready.append(li)
    return csv_ready

def uploadCSV(filename, csv_ready):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for row in csv_ready:
            writer.writerow(row)

def getBoundsMatrix(pts, grid_size = .4):

    #create the map matrix
    max_x = round(max(point[0] for point in pts), 1)
    min_x = round(min(point[0] for point in pts), 1)
    max_y = round(max(point[1] for point in pts), 1)
    min_y = round(min(point[1] for point in pts), 1)
    floatify = .0000001
    y_ranges = []
    y = max_y + grid_size / 2
    while y >= min_y - grid_size:
        y_ranges.append(y)
        y -= grid_size 

    x_ranges = []
    x = min_x - grid_size / 2
    while x <= max_x + grid_size:
        x_ranges.append(x)
        x += grid_size 
    
    matrix = []
    for r, row_range in enumerate(y_ranges):
        if r > 0:
            l = []
            for c, col_range in enumerate(x_ranges):
                if c > 0:
                    x_bounds = [round(x_ranges[c-1], 8), round(col_range - floatify, 8)]
                    y_bounds = [round(row_range, 8), round(y_ranges[r-1] - floatify, 8)]
                    bounds = {"x": x_bounds, "y": y_bounds, "tag":0, "pts": None}
                    l.append(bounds)
            matrix.append(l)
    return matrix


#[(x,y), ...], floats are allowed
#units are in meters
#grid size is defined by .40, .40
def getMap(filename, points, hazards):
    #convert points into array of arrays [[x,y], ...] round all items to 2 decimal places
    
    pts = [[round(tup[0], 4), round(tup[1], 4)] for tup in points]
    bounding_pts = pts.copy()
    haz = {}

    if len(hazards) > 0:
        haz = {k: list(v) for k, v in hazards.items()}
        for name, h in haz.items():
            bounding_pts.append(h)

    bounds_matrix = getBoundsMatrix(bounding_pts)
    points_matrix = addPoints(pts, bounds_matrix)

    makeLines(points, points_matrix)
    lines_matrix = points_matrix
    if len(hazards) > 0:
        addHazards(haz, lines_matrix)

    lines_hazards_matrix = lines_matrix
    csv_ready = simplifyMatrix(lines_hazards_matrix)
    uploadCSV(filename, csv_ready)
    
    return csv_ready

#bounds matrix should also include the hazard points extremes
# points = [[0, 0], [0, 1], [0, 2], [3, 2]]
# hazards = {"magnet": (2,1), "heat": (0, .5)}
# filename = "matrix.csv"
# my_map = getMap(filename, points, hazards)
# for r in my_map:
#     print(r)

# points = [[0, 0], [0, 1.0004], [0, 2.005], [3, 2], [3.1, -1]]
# hazards = {"magnet": (-4,6), "heat": (0, .5)}
# filename = "matrix1.csv"
# my_map = getMap(filename, points, hazards)
# for r in my_map:
#     print(r)


#points = [(0,0),(1,0),(2,0),(2,2),(0,2), (0, 3), (-2,2),(0,2), ()]
points = [(0,0),(0,1), (0,2), (2, 2), (2, 1.5), (2,2), (0, 2), (-1.5, 2), (0,2), (0,1), (-1, 1)]

hazards = {"magnet1": (-1.5,2), "heat1": (2, 1.5)}
filename = "matrix1.csv"
my_map = getMap(filename, points, hazards)
for r in my_map:
    print(r)

# points = [[0, 0], [-0.0103, 0.2961], [-0.0553, 1.1531], [-0.0617, 1.2753], [0.233, 1.2856], [0.5567, 1.3025], [0.6188, 1.3047], [1.2993, 1.3404]]
# hazards = {}
# filename = "matrix.csv"
# my_map = getMap(filename, points, hazards)
# for r in my_map:
#     print(r)

# points = (0, 0), (-0.0103, 0.2961), (-0.0553, 1.1531), (-0.0617, 1.2753), (0.233, 1.2856), (0.5567, 1.3025), (0.6188, 1.3047), (1.2993, 1.3404)
