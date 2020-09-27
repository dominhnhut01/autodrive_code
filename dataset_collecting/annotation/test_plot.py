import matplotlib.pyplot as plt
import numpy as np
import math
x = np.arange(0,math.pi*2,0.005)
y = np.sin(x)

plt.plot(x,y)

plt.show()
