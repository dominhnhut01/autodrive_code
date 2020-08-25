import numpy as np
import PIL
from PIL import Image
import matplotlib.pyplot as plt

img = Image.open('E:/college_projects/autodrive_car/dataset/output_tif/street_centerline_NYC_102.tif')

img_arr = np.array(img)


print(img_arr.shape[0],img_arr.shape[1])
print('Done')

