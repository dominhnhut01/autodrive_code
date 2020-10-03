import os
from osgeo import osr,gdal

def jp2_to_tif(in_direc,out_direc)	
	for file in os.listdir(in_direc):
		name = file[0:-4]
		print(name)
		in_file = '{}/{}'.format(in_direc,file)
		out_file = '{}/{}.tif'.format(out_direc,name)
		os.system("gdal_translate {} {}".format(in_file,out_file))
		Img_ref = gdal.Open(in_file)
		Img = gdal.Open((out_file))
		wkt = Img_ref.GetProjection()
		srs = osr.SpatialReference()
		srs.ImportFromWkt(wkt)
		Img.SetProjection(srs.ExportToWkt())
	for file in os.listdir(out_direc):
	    if (file[-3:]!="tif"):
	        os.remove("{}/{}".format(out_direc,file))

if __name__ = '__main__':
	os.chdir('../../dataset/')
	main_dir = os.getcwd()
	in_folder = input("Enter input folder name here: ")
	out_folder = input("Enter output folder name here: ")
	in_direc = os.path.join(main_dir,in_folder)
	out_direc = os.path.join(main_dir,out_folder)
	jp2_to_tif(in_direc,out_direc)