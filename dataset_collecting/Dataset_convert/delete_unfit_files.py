import os

def delete(ref_dir,processed_dir):
	'''
	This function will delete all files in the processed folder 
	that have different number components from those from the reference folder, 
	to ensure every file in each folder is in a pair with a file in the another folder.
	For example:
		Reference folder:
		- street_data_1.npy
		- street_data_3.npy
		- street_data_100.npy
		- street_data_1000.npy
		Processed folder:
		- NYC_1.tif
		- NYC_3.tif
		- NYC_4.tif
		- NYC_77.tif
		- NYC_100.tif
		- NYC_140.tif
		- NYC_1000.tif
		File will be deleted:
		- NYC_4.tif
		- NYC_77.tif
		- NYC_140.tif
	Param:
	- ref_dir: Directory of the reference folder.
	- processed_dir: Directory of the folder you want to process.
	'''

	ref_files = os.listdir(ref_dir)
	for i in range(len(ref_files)):
		temp = ref_files[i]
		ref_files[i]='NYC_{}.tif'.format(temp[12:-4])
	print(ref_files)
	for npy_file in os.listdir(processed_dir):
		if npy_file not in ref_files:
			try:
				os.remove('{}/{}'.format(processed_dir,npy_file))
				print('Done')
			except:
				continue
				
if __name__ == '__main__':
	ref_dir = input('Input the directory of your jpg folder: ')
	processed_dir = input('Input the directory of your npy folder: ')
	delete(ref_dir,processed_dir)