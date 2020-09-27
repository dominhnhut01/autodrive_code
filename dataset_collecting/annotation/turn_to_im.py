import numpy as np
from PIL import Image
import os

files = "/home/tsoi/Yours/Projects/SDC/data/array"
out_folder = "/home/tsoi/Yours/Projects/SDC/data/original_image"
for file in os.listdir(files):
        im = np.load(files+"/" + file)
        img = Image.fromarray(im)
        img.save("/home/tsoi/Yours/Projects/SDC/data/not_eliminated_image/{}.jpg".format(file))


'''
num = 207
file = "street_data_"+str(num)+".npy"
im = np.load("./dummy" +"/"+ file)
#im = np.load("./array" +"/"+ file)
name = file[:-4]
img = Image.fromarray(im)
img.save(./output_image/{}.jpg.format(name))
'''
