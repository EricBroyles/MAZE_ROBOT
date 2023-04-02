points = [(0,0), (0,4), (-1,4), (2,4)]


def findIndex(matrix, target):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == target:
                return (i, j)
    # target not found
    print("return none: ", target)
    return None
# determine size of matrix
max_x = max(point[0] for point in points)
min_x = min(point[0] for point in points)
max_y = max(point[1] for point in points)
min_y = min(point[1] for point in points)
matrix_size = (max_x - min_x + 1, max_y - min_y + 1)

matrix = []

for row in range(matrix_size[1]):
    list =[]
    for col in range(matrix_size[0]):
        val = 0
        pt = (min_x + col, max_y - row)
        
        if pt in points:
            val = pt
            

        list.append(val)
    matrix.append(list)

for row in matrix:
    print(row)

new_matrix = matrix.copy()

for index_pt in range(1, len(points)):
    (prev_row, prev_col) = findIndex(new_matrix, points[index_pt - 1])
    (row, col) = findIndex(new_matrix, points[index_pt])

    print((prev_row, prev_col), (row, col))

    row_inc = 1 if row > prev_row else -1
    col_inc = 1 if col > prev_col else -1

    for row in range(prev_row, row + row_inc, row_inc):
        for col in range(prev_col, col + col_inc, col_inc):
            matrix[row][col] = 1

    for row in matrix:
        print(row)


for row in matrix:
    print(row)
