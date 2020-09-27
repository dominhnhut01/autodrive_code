from libtiff import TIFF
import numpy as np
import os
def tif_to_npy(st_line_direc,st_centerline_direc,out_direc):	
	for file in os.listdir(st_line_direc):
	#Loop over each file in the input directory
		if (file[-3:]=="tif"):
			fn = file[0:-4]
			tif = TIFF.open('{}/{}'.format(st_line_direc, file))
			image = tif.read_image()
			np.save('{}/{}.npy'.format(out_direc,fn),image)
		else:
			continue
	for file in os.listdir(st_centerline_direc):
	#Loop over each file in the input directory
		if (file[-3:]=="tif"):
			fn = file[0:-4]
			tif = TIFF.open('{}/{}'.format(st_centerline_direc, file))
			image = tif.read_image()
			np.save('{}/{}.npy'.format(out_direc,fn),image)
		else:
			continue
def merge_npy(out_direc):
	file_num = len(os.listdir(out_direc))
	fn_pair = []
	for i in range(int(file_num/2)):
		st_line = np.load('{}/street_line_NYC_NYC_{}.npy'.format(out_direc,i+1))
		st_centerline = 2*np.load('{}/street_centerline_NYC_NYC_{}.npy'.format(out_direc,i+1))
		st_data = st_line+st_centerline
		width,length=st_data.shape
		for y in range(width):
			for x in range(length):
				if st_data[y][x] >2:
					st_data[y][x]=2
		
		np.save('{}/street_data_{}.npy'.format(out_direc,i+1),st_data)
		
		os.remove('{}/street_line_NYC_NYC_{}.npy'.format(out_direc,i+1))
		os.remove('{}/street_centerline_NYC_NYC_{}.npy'.format(out_direc,i+1))
if __name__ == '__main__':
	st_line_direc = input("Enter street line directory here: ")
	st_centerline_direc = input("Enter street centerline directory here: ")
	out_direc = input("Enter output data directory here: ")
	tif_to_npy(st_line_direc,st_centerline_direc,out_direc)
	print('Merging.........................')
	merge_npy(out_direc)
	print('Done!')