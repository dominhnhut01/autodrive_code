import numpy as np
import os

folder = "/home/tsoi/Yours/Projects/SDC/data/array"
out_folder = "/home/tsoi/Yours/Projects/SDC/data/eliminated_array"
percentage = 0.8
threshold = 100

for file in os.listdir(folder):
    try:
        imap = np.load(folder+"/"+file)
        if not (np.count_nonzero(imap==1)<threshold):
            np.save(out_folder+"/"+file,imap)
    except:
        continue
