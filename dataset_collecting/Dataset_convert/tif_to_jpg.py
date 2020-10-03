import os
#Requirement package: gdal

def tif_to_jpg(in_dir,out_dir):
	'''
	This function would convert all the .tif files in the input folder to .jpg file, which would be put in the output folder
	Param:
	- in_dir: The directory of the input folder (folder of .tifnpy files)
	- out_dir: The directory of the output folder (folder of .jpg files)
	Return: This function return nothing
	'''	
	for file in os.listdir(in_dir):
	    name = file[0:-4]
	    print(name)
	    print("gdal_translate -of JPEG -scale -co worldfile=yes {}/{} {}/{}.jpg".format(in_dir,file,out_dir,name))
	    os.system("gdal_translate -of JPEG -scale -co worldfile=yes {}/{} {}/{}.jpg".format(in_dir,file,out_dir,name))

	for file in os.listdir(out_dir):
	    if (file[-3:]!="jpg"):
	        os.remove("{}/{}".format(out_dir,file))

if __name__ == '__main__':
	#Get the current directory
	os.chdir('../../../dataset/')
	main_dir = os.getcwd()
	in_folder = input("Enter input folder name here: ")
	out_folder = input("Enter output folder name here: ")
	
	#Create absolute path:
	in_dir = os.path.join(main_dir,in_folder)
	out_dir = os.path.join(main_dir,out_folder)
	tif_to_jpg(in_dir,out_dir)
