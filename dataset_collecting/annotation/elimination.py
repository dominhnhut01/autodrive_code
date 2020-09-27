import numpy as np
import os
import matplotlib.pyplot as plt
folder = "/home/tsoi/Yours/Projects/SDC/data/fixed_array"
out_folder = "/home/tsoi/Yours/Projects/SDC/data/not_eliminated_array"
percentage = 0.8
threshold = 100
points = []
for file in os.listdir(folder):
    try:
        imap = np.load(folder+"/"+file)
        registered_point = np.count_nonzero(imap == 255)
        ratio = registered_point/imap.size
        if (ratio>=0.2 and ratio<=0.6):
            np.save(out_folder+"/"+file,imap)
    except:
        continue

#x = points
#x.sort()
#range(len(x))
#range(len(points))
#plt.scatter(range(len(points)),x)
#plt.show()
