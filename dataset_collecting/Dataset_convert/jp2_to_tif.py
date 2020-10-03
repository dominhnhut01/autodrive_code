import os
from osgeo import osr,gdal

def jp2_to_tif(in_dir,out_dir):
	'''
	This function would convert all the .jp2 files in the input folder to .tif file, which would be put in the output folder
	Param:
	- in_dir: The directory of the input folder (folder of .jp2 files)
	- out_dir: The directory of the output folder (folder of .tif files)
	Return: This function return nothing
	'''	
	
	#Loop through every file in the input folder directory
	for file in os.listdir(in_dir):
		name = file[0:-4]
		in_file = '{}/{}'.format(in_dir,file)
		out_file = '{}/{}.tif'.format(out_dir,name)
		#Convert jp2 to tif
		os.system("gdal_translate {} {}".format(in_file,out_file))

		#Transfer the projection and coordinate system information from the jp2 file to the tif file
		Img_ref = gdal.Open(in_file)
		Img = gdal.Open((out_file))
		wkt = Img_ref.GetProjection()
		srs = osr.SpatialReference()
		srs.ImportFromWkt(wkt)
		Img.SetProjection(srs.ExportToWkt())

	#Remove unwanted output file	
	for file in os.listdir(out_dir):
	    if (file[-3:]!="tif"):
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
	jp2_to_tif(in_dir,out_dir)