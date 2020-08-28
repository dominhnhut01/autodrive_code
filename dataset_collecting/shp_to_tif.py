# A script to rasterise a shapefile to the same projection & pixel resolution as a reference image.
from osgeo import ogr, gdal
import subprocess
import os

def shp_to_tif():
	ref_dir_list = []
	folder = 'E:/college_projects/autodrive_car/dataset/output_tif/raw_dataset/NYC'
	for filename in os.listdir(folder):
	    if ".tif" in filename:
	        ref_dir_list.append(filename)
	    else:
	        continue
	InputVector = 'E:/college_projects/autodrive_car/dataset/NYC_citymap/citymap_streetcenterlines_v1.shp'
	for ref_file_name in ref_dir_list:
		try:
			ref_dir = os.path.join(folder,ref_file_name)
			OutputImage = 'E:/college_projects/autodrive_car/dataset/output_tif/street_centerline/street_centerline_{}'.format(ref_file_name)

			gdalformat = 'GTiff'
			datatype = gdal.GDT_Byte
			burnVal = 1 #value for the output image pixels
			##########################################################
			# Get projection info from reference image
			Image = gdal.Open(ref_dir, gdal.GA_ReadOnly)

			# Open Shapefile
			Shapefile = ogr.Open(InputVector)
			Shapefile_layer = Shapefile.GetLayer()

			# Rasterise
			print("Rasterising shapefile...")
			Output = gdal.GetDriverByName(gdalformat).Create(OutputImage, Image.RasterXSize, Image.RasterYSize, 1, datatype, options=['COMPRESS=DEFLATE'])
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
	shp_to_tif()
	print("Done.")