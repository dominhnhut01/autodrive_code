import numpy as np
import os
files = "./array"
dummy = "./dummy"
for file in os.listdir(files):
    imap = np.load(files+"/"+file)
    length = imap.shape[1]
    width = imap.shape[0]
    for y in range(width):
        for x in range(length):
            if(imap[y][x]==2):
                imap[y][x]=255
            if (imap[y][x]==1):
                imap[y][x]=100
    np.save(dummy+"/"+file,imap)
