import numpy as np
from PIL import Image
import os

#in_direc = "/home/tsoi/Yours/Projects/SDC/data/array"
#out_direc = "/home/tsoi/Yours/Projects/SDC/data/original_image"

in_direc = input("Enter input data directory here: ")
out_direc = input("Enter output data directory here: ")
for file in os.listdir(in_direc):
        im = np.load(in_direc+"/" + file)
        img = Image.fromarray(im)
        img.save("{}/{}.jpg".format(out_direc,file[:-4]))


'''
num = 207
file = "street_data_"+str(num)+".npy"
im = np.load("./dummy" +"/"+ file)
#im = np.load("./array" +"/"+ file)
name = file[:-4]
img = Image.fromarray(im)
img.save(./output_image/{}.jpg.format(name))
'''
