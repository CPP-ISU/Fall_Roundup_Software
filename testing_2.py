import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

# Sample data
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x) + np.random.normal(0, 0.1, 100)  # Adding some noise to the signal

# Smooth the data using savgol_filter
smoothed_y = savgol_filter(y, window_length=11, polyorder=2)

# Plot the original and smoothed data
plt.plot(x, y, label='Original Data')
plt.plot(x, smoothed_y, label='Smoothed Data')
plt.legend()
plt.show()

