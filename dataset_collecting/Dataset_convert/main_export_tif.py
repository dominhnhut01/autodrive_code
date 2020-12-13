from osgeo import gdal, osr
import os
import numpy as np
import random

class Region_Division:
    '''
    This class is used to hold and generate new coordinate information of the input tif file.
    Param:
    - region_coor: the list of the input region's coordinate in the format [min_x, min_y, max_x, max_y]
    - return_size: the desired size of the smaller output tif file
    Functions:
    - rescale(): rescale the given tif file for later region division
    - divide(): divide the big tif into smaller ones
    '''
    def __init__(self, region_coor,returned_size):
        #Enter the initial region's coordinate and returned size(width in longtitude and height in latitude)
        self.region_coor = region_coor
        self.rescaled_region = np.zeros(4)
        self.returned_size=returned_size
    def rescale(self):
        #Rescale the region coordinates. Add coordinates of new small regions into self.rescaled_region
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

    def rand_int(self):
        return int(random.choice((1,2)))
    def divide(self):
        #Divide the initial region's into smaller ones. Return a np.array of coordinates of small regions
        self.rescale()
        column = int(self.rescaled_width//self.returned_size[0]) #number of column
        row = int(self.rescaled_height//self.returned_size[1]) #number of row
        self.divided_region = np.zeros((row*column,4))
        coor_num=0
        for y in range(row):
            for x in range(column):
                i = self.rand_int()
                if i==2:
                    self.divided_region[coor_num][0] = self.rescaled_region[0] + self.returned_size[0]*x
                    self.divided_region[coor_num][1] = self.rescaled_region[1] + self.returned_size[1]*y
                    self.divided_region[coor_num][2] = self.rescaled_region[0] + self.returned_size[0]*(x+1)
                    self.divided_region[coor_num][3] = self.rescaled_region[1] + self.returned_size[1]*(y+1)   
                else:
                    self.divided_region[coor_num][0] = -1
                    self.divided_region[coor_num][1] = -1
                    self.divided_region[coor_num][2] = -1
                    self.divided_region[coor_num][3] = -1
                print('{} rows {} columns'.format(y+1,x+1))
                coor_num+=1
        return self.divided_region

def random_dimension(returned_width_list,returned_height_list):
    returned_width=int(random.choice(returned_width_list))
    returned_height=int(random.choice(returned_height_list))
    return [returned_width,returned_height]

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
        returned_width_list=[350,400,430,470,490,530]
        returned_height_list=[180,200,220,250,270,290,360]
        returned_size=random_dimension(returned_width_list,returned_height_list)
        #Create the list of small GEOTIFF's coordinate
        region_obj = Region_Division(region_coor,returned_size)
        divided_region = region_obj.divide()

        #Export the small GEOTIFF
        for coor in divided_region:
            if coor[0]!=-1:
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
    #Get the current directory
    os.chdir('../../../dataset/')
    main_dir = os.getcwd()
    in_folder = input("Enter input folder name here: ")
    out_folder = input("Enter output folder name here: ")
    
    #Create absolute path:
    input_dir = os.path.join(main_dir,in_folder)
    output_dir = os.path.join(main_dir,out_folder)
    export_tif(input_dir,output_dir)
    print('End of program')