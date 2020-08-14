from osgeo import gdal, osr
from region_divide import region_divide
import os

def export_tif():
    
    tif_dir = []
    folder = 'E:/College projects/Autodrive car/autodrive_code/dataset_collecting/dataset/input_tif'
    for filename in os.listdir(folder):
        if ".tif" in filename:
            filename = os.path.join(folder,filename)
            tif_dir.append(filename)
        else:
            continue
    
    #Small GEOTIFF's index
    num=1
    
    #Loop over each large GEOTIFF
    for filename in tif_dir:
        driver = gdal.GetDriverByName('GTiff')

        dataset = gdal.Open(filename)
        band = dataset.GetRasterBand(1)

        transform = dataset.GetGeoTransform()
        width = dataset.RasterXSize
        height = dataset.RasterYSize

        #Find the minimum and maximum longtitude and latitude of the GEOTIFF
        min_x = transform[0]
        min_y = transform[3] + width*transform[4] + height*transform[5] 
        max_x = transform[0] + width*transform[1] + height*transform[2]
        max_y = transform[3]
        
        region_coor = [min_x, min_y, max_x, max_y]
        dimension = [436,220]
        
        #Create the list of small GEOTIFF's coordinate
        region_obj = region_divide(region_coor,dimension)
        divided_region = region_obj.divide()

        #Export the small GEOTIFF
        for coor in divided_region:
            try:    
                p1 = (coor[0], coor[3])
                p2 = (coor[2], coor[1])

                xOrigin = transform[0]
                yOrigin = transform[3]
                pixelWidth = transform[1]
                pixelHeight = -transform[5]


                i1 = int((p1[0] - xOrigin) / pixelWidth)
                j1 = int((yOrigin - p1[1] ) / pixelHeight)
                i2 = int((p2[0] - xOrigin) / pixelWidth)
                j2 = int((yOrigin - p2[1]) / pixelHeight)


                new_cols = i2-i1+1
                new_rows = j2-j1+1

                data = band.ReadAsArray(i1, j1, new_cols, new_rows)

                new_x = xOrigin + i1*pixelWidth
                new_y = yOrigin - j1*pixelHeight

                new_transform = (new_x, transform[1], transform[2], new_y, transform[4], transform[5])

                # Create gtif file 
                driver = gdal.GetDriverByName("GTiff")

                output_file = 'E:/College projects/Autodrive car/autodrive_code/dataset_collecting/dataset/output_tif/img_{}.tif'.format(num)

                dst_ds = driver.Create(output_file, 
                                       new_cols, 
                                       new_rows, 
                                       1, 
                                       gdal.GDT_Float32)

                #writting output raster
                dst_ds.GetRasterBand(1).WriteArray( data )

                #setting extension of output raster
                # top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
                dst_ds.SetGeoTransform(new_transform)

                wkt = dataset.GetProjection()

                # setting spatial reference of output raster 
                srs = osr.SpatialReference()
                srs.ImportFromWkt(wkt)
                dst_ds.SetProjection( srs.ExportToWkt() )
                print('Created {} file(s)'.format(num))
                num+=1
            except:
                continue
        #Close dataset
        dataset = None
        dst_ds = None

if __name__ == '__main__':
	export_tif()
	print('End of program')