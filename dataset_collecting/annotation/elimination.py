import numpy as np
import os
import matplotlib.pyplot as plt
#in_direc = "/home/tsoi/Yours/Projects/SDC/data/fixed_array1"
#out_direc = "/home/tsoi/Yours/Projects/SDC/data/fixed_array2"
in_direc = input("Enter input data directory here: ")
out_direc = input("Enter output data directory here: ")

percentage = 0.8
threshold = 100
points = []

for file in os.listdir(in_direc):
    try:
        imap = np.load(in_direc+"/"+file)
        registered_point = np.count_nonzero(imap == 255)
        ratio = registered_point/imap.size
        #points.append(ratio)
        if (ratio>0.01 and ratio<=0.7):
            np.save(out_direc+"/"+file,imap)
    except:
        continue
'''
x = points
x.sort()
range(len(x))
range(len(points))
plt.scatter(range(len(points)),x)
plt.show()
'''