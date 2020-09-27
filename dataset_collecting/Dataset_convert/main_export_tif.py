from osgeo import gdal, osr
import os
import numpy as np

class region_divide:
    def __init__(self, region_coor, returned_size):
        #Enter the initial region's coordinate and returned size(width in longtitude and height in latitude)
        self.region_coor = region_coor
        self.returned_size = returned_size
        self.rescaled_region = np.zeros(4)

    def rescale(self):
        #Rescale the region coordinates
        self.rescaled_width = ((self.region_coor[2]-self.region_coor[0])//self.returned_size[0])*self.returned_size[0]
        self.rescaled_height = ((self.region_coor[3]-self.region_coor[1])//self.returned_size[1])*self.returned_size[1]
        
        #Ensure height and width are positive
        if self.rescaled_height<0:
            self.rescaled_height=-self.rescaled_height
        if self.rescaled_width<0:
            self.rescaled_width=-self.rescaled_width
        
        #Append new coordinates to the list
        self.rescaled_region[0] = self.region_coor[0]
        self.rescaled_region[1] = self.region_coor[1]
        self.rescaled_region[2] = self.region_coor[0]+self.rescaled_width
        self.rescaled_region[3] = self.region_coor[1]+self.rescaled_height

    def divide(self):
        #Divide the initial region's into smaller one. Return a np.array of coordinates of small regions
        self.rescale()
        column = int(self.rescaled_width//self.returned_size[0]) #number of column
        row = int(self.rescaled_height//self.returned_size[1]) #number of row
        self.divided_region = np.zeros((row*column,4))
        coor_num = 0
        for y in range(row):
            for x in range(column):
                self.divided_region[coor_num][0] = self.rescaled_region[0] + self.returned_size[0]*x
                self.divided_region[coor_num][1] = self.rescaled_region[1] + self.returned_size[1]*y
                self.divided_region[coor_num][2] = self.rescaled_region[0] + self.returned_size[0]*(x+1)
                self.divided_region[coor_num][3] = self.rescaled_region[1] + self.returned_size[1]*(y+1)   
                print('{} rows {} columns'.format(y+1,x+1))
                coor_num +=1
        return self.divided_region

def export_tif(input_dir,output_dir):
#Export small tiff files from large tiff
    tif_dir = []
    for filename in os.listdir(input_dir):
        if ".tif" in filename:
            filename = os.path.join(input_dir,filename)
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

                output_file = '{}/NYC_{}.tif'.format(output_dir,num)

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
    input_dir = input("Enter input data directory here: ")
    output_dir = input("Enter output data directory here: ")
    export_tif(input_dir,output_dir)
    print('End of program')