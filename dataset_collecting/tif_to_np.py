from libtiff import TIFF
import numpy as np
import os
direc = input("Enter input data directory here: ")
out_direc = input("Enter output data directory here: ")
for file in os.listdir(direc):
	if (file[-3:]=="tif"):
		name = file[0:-4]
		tif = TIFF.open('{}/{}'.format(direc, file))
		image = tif.read_image()
		np.save('{}/{}.npy'.format(out_direc,name),image)
	else:
		continue

