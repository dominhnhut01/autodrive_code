import os
from osgeo import osr,gdal

#direc = "./input"
#out_direc = "~/Yours/Projects/SDC/dataset/output"
in_direc = input("Enter input data directory here: ")
out_direc = input("Enter output data directory here: ")
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