import matplotlib.pyplot as plt

# Data
x = [1, 2, 3, 4, 5]  # First array of numbers
y1 = [10, 5, 8, 3, 6]  # Second array of numbers
y2 = [(8, 4), (4, 2), (7, 3), (3, 1), (5, 2)]  # Array of tuples

# Create a figure and axis object
fig, ax = plt.subplots()

# Plot the first dataset (array of numbers)
ax.plot(x, y1, label='Dataset 1')

# Plot the second dataset (array of tuples)
for i in range(len(y2[0])):
    y = [t[i] for t in y2]
    ax.plot(x, y, label='Dataset 2 Line {}'.format(i+1))

# Plot the third dataset (array of numbers)
ax.plot(x, y2, label='Dataset 3')

# Set axis labels and title
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('Three Datasets on Same Graph')

# Add a legend
ax.legend()

# Show the plot
plt.show()