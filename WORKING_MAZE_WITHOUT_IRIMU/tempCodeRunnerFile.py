points = [[0, 0], [-0.0103, 0.2961], [-0.0553, 1.1531], [-0.0617, 1.2753], [0.233, 1.2856], [0.5567, 1.3025], [0.6188, 1.3047], [1.2993, 1.3404]]
hazards = {}
filename = "matrix.csv"
my_map = getMap(filename, points, hazards)
for r in my_map:
    print(r)