from libtiff import TIFF
import numpy as np
import os
def tif_to_npy(st_line_dir,st_centerline_dir,out_dir):	
	'''
	This function would convert all the .tif files in the street line and street centerline folder to .npy file, which would be put in the output folder
	Param:
	- st_line_dir: The directory of the street line folder
	- st_centerline_dir: The directory of the street centerline folder
	- out_dir: The directory of the output folder (folder of .npy files)
	Return: This function return nothing
	'''	
	for file in os.listdir(st_line_dir):
	#Loop over each file in the input directory
		if (file[-3:]=="tif"):
			fn = file[0:-4]
			tif = TIFF.open('{}/{}'.format(st_line_dir, file))
			image = tif.read_image()
			np.save('{}/{}.npy'.format(out_dir,fn),image)
		else:
			continue
	for file in os.listdir(st_centerline_dir):
	#Loop over each file in the input directory
		if (file[-3:]=="tif"):
			fn = file[0:-4]
			tif = TIFF.open('{}/{}'.format(st_centerline_dir, file))
			image = tif.read_image()
			np.save('{}/{}.npy'.format(out_dir,fn),image)
		else:
			continue
def merge_npy(out_dir):
	file_num = len(os.listdir(out_dir))
	fn_pair = []
	for i in range(int(file_num/2)):
		st_line = np.load('{}/streetline_NYC_{}.npy'.format(out_dir,i+1))
		st_centerline = 2*np.load('{}/street_centerline_NYC_{}.npy'.format(out_dir,i+1))
		st_data = st_line+st_centerline
		width,length=st_data.shape
		for y in range(width):
			for x in range(length):
				if st_data[y][x] >2:
					st_data[y][x]=2
		
		np.save('{}/NYC_{}.npy'.format(out_dir,i+1),st_data)
		
		os.remove('{}/streetline_NYC_{}.npy'.format(out_dir,i+1))
		os.remove('{}/street_centerline_NYC_{}.npy'.format(out_dir,i+1))
if __name__ == '__main__':
	#Get the current directory
	os.chdir('../../../dataset/')
	main_dir = os.getcwd()
	
	st_line_folder = input("Enter street line folder here: ")
	st_centerline_folder = input("Enter street centerline folder here: ")
	out_folder = input("Enter output data folder here: ")

	#Create absolute path:
	st_line_dir = os.path.join(main_dir,st_line_folder)
	st_centerline_dir = os.path.join(main_dir,st_centerline_folder)
	out_dir = os.path.join(main_dir,out_folder)


	#tif_to_npy(st_line_dir,st_centerline_dir,out_dir)
	print('Merging.........................')
	merge_npy(out_dir)
	print('Done!')