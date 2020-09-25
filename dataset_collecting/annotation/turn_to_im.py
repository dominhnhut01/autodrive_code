import numpy as np
from PIL import Image
import os

files = "./fixed_array"
for file in os.listdir(files):
    im = np.load(files+"/" + file)
    img = Image.fromarray(im)
    img.save('./output_image/{}.png'.format(file))

'''
num = 207
file = "street_data_"+str(num)+".npy"
im = np.load("./dummy" +"/"+ file)
#im = np.load("./array" +"/"+ file)
name = file[:-4]
img = Image.fromarray(im)
img.save('./output_image/{}.jpg'.format(name))
'''
