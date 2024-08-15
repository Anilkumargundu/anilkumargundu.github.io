import matplotlib.pyplot as plt
from scipy.special import erfc
import numpy as np

def Q(x):
    return 0.5 * erfc(x / np.sqrt(2))

# Get 10 user-defined values in a single input
user_input = input("Please enter 10 values separated by spaces: ")

# Split the input string into a list of strings and convert each to a float
user_values = list(map(float, user_input.split()))

# Ensure the user provided exactly 10 values
if len(user_values) != 10:
    raise ValueError("Please enter exactly 10 values.")

# Convert user-defined values to a numpy array
x_values = np.array(user_values)

# Calculate Q(x) for each value in the array
q_values = Q(x_values)

# Print each Q(x) value with a precision of 25 digits
for x, q in zip(x_values, q_values):
    print(f"Q({x}) = {q:.25f}")

# Plotting the values Q(x) as a bar graph
plt.bar(x_values, q_values, color='blue', edgecolor='black')
plt.xlabel('x values')
plt.ylabel('Q(x) values')
plt.title('Q(x) Bar Graph')
plt.show()
