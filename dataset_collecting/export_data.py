import numpy as np
from region_divide import region_divide

import ee

def export_data(txt_dir):
  #Read coordinates from the text file
  coor_list = []
  with open (txt_dir,'rt') as coor_src:
    i = 0
    for line in coor_src:
      if line[0] == '#': #Skip the comments
        continue
      coor_list.append(line.split(';'))
      coor_list[i]=[float(x) for x in coor_list[i]]
      i+=1

  #Initialize the Earth Engine account
  ee.Initialize()
  print('Initialize successfully')
  #Initialize constants
  dimension = (0.04514694,0.01829339)
  img_num = 0
  
  #Exporting data
  for region_coor in coor_list:
    region_obj = region_divide(region_coor,dimension)
    divided_region = region_obj.divide()
    
    for y in range(shape[0]):
        for x in range(shape[1]):
            img_num+=1
            region = ee.Geometry.Rectangle(list(divided_region[y][x]))
            dataset = ee.ImageCollection('COPERNICUS/S2_SR')\
                      .filterDate('2019-01-01', '2020-01-30')\
                      .filterBounds(region)\
                      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))
        
        
            
            img = dataset.select("B4","B3","B2").median().clip(region).divide(10000).select("B4","B3","B2")
            task = ee.batch.Export.image.toDrive(
              image= img,
              description= 'img_{}'.format(img_num),
              scale= 10,
              folder= 'GEOTIFF',
              maxPixels= 1e12,
              region= region
            )
            task.start()
            print('Exported {} image(s)'.format(img_num))
