import numpy as np
from PIL import Image
import os

def npy_to_png(in_dir,out_dir):
	'''
	This function would convert all the .npy files in the input folder to .png file, which would be put in the output folder
	Param:
	- in_dir: The directory of the input folder (folder of .npy files)
	- out_dir: The directory of the output folder (folder of .png files)
	Return: This function return nothing
	'''	
	for file in os.listdir(in_dir):
		im = np.load(in_dir+"/" + file)
		img = Image.fromarray(im)
		img.save("{}/{}.png".format(out_dir,file[:-4]))

def color_index(npy_dir):
	for file in os.listdir(npy_dir):
		arr = np.load(npy_dir+"/"+file)
		arr = np.where(arr==255,1,arr)
		np.save(npy_dir+"/"+file,arr)


if __name__ == '__main__':
	#Get the current directory
	os.chdir('../../../dataset/')
	main_dir = os.getcwd()
	in_folder = input("Enter input folder name here: ")
	out_folder = input("Enter output folder name here: ")
	color_index_ans = input("Do you want to convert the npy files into color indexed file? (Yes/No): ")

	#Create absolute path:
	in_dir = os.path.join(main_dir,in_folder)
	out_dir = os.path.join(main_dir,out_folder)
	if color_index_ans=="Yes":
		color_index(in_dir)
	npy_to_png(in_dir,out_dir)