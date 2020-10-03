# A script to rasterise a shapefile to the same projection & pixel resolution as a reference image.
from osgeo import ogr, gdal
import subprocess
import os

def shp_to_tif(shp_dir,ref_dir,out_dir):
	'''
	This function would convert a big shp file to smaller tif files based on the georeference from the reference .tif files.
	Param:
	- sh_dir: The directory of the shp file
	- ref_dir: The directory of the folder of reference .tif files
	- out_dir: The directory of the folder which contains the output .tif files
	Return: This function return nothing
	'''	
	
	ref_dir_list = []
	for filename in os.listdir(ref_dir):
	    if ".tif" in filename:
	        ref_dir_list.append(filename)
	    else:
	        continue
	for ref_file_name in ref_dir_list:
		try:
			ref_file_dir = os.path.join(ref_dir,ref_file_name)
			OutputImage = '{}/street_centerline_{}'.format(out_dir,ref_file_name)

			gdalformat = 'GTiff'
			datatype = gdal.GDT_Byte
			burnVal = 1 #value for the output image pixels
			##########################################################
			# Get projection info from reference image
			Image = gdal.Open(ref_file_dir, gdal.GA_ReadOnly)

			# Open Shapefile
			Shapefile = ogr.Open(shp_dir)
			Shapefile_layer = Shapefile.GetLayer()

			# Rasterise
			print("Rasterising shapefile...")
			Output = gdal.GetDriverByName(gdalformat).Create(OutputImage, Image.RasterXSize, Image.RasterYSize, 1, datatype, options=['COMPRESS=DEFLATE'])
			
			# Transfer the projection and coordinate system information
			Output.SetProjection(Image.GetProjectionRef())
			Output.SetGeoTransform(Image.GetGeoTransform())


			# Write data to band 1
			Band = Output.GetRasterBand(1)
			Band.SetNoDataValue(0)
			gdal.RasterizeLayer(Output, [1], Shapefile_layer, burn_values=[burnVal])

			# Close datasets
			Band = None
			Output = None
			Image = None
			Shapefile = None

			# Build image overviews
			subprocess.call("gdaladdo --config COMPRESS_OVERVIEW DEFLATE "+OutputImage+" 2 4 8 16 32 64", shell=True)
			print('Exported {}'.format(ref_file_name))
		except:
			continue

if __name__ == '__main__':
	shp_file = input("Enter shp folder and file here (ex: NYC_citymap/citymap_citymap_v1.shp): ")
	ref_folder = input("Enter reference geotiff files folder here: ")
	out_folder = input("Enter output files folder here: ")
	
	#Get the current directory
	os.chdir('../../../dataset/')
	main_dir = os.getcwd()
	
	#Create absolute path:
	shp_dir = os.path.join(main_dir,shp_file)
	ref_dir = os.path.join(main_dir,ref_folder)
	out_dir = os.path.join(main_dir,out_folder)

	shp_to_tif(shp_dir,ref_dir,out_dir)
	print("Done.")