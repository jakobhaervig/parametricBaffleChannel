import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('results.csv', delimiter=',', skiprows=1, usecols=(0, 1, 2, 3, 4), unpack=True)

plt.plot(data[3], data[4],'s', markersize=5, color='blue')



plt.show()