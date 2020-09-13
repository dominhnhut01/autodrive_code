import numpy as np
from PIL import Image
import os

files = "./street_data_np - Copy/"
for file in os.listdir(files):
    im = np.load(files + file)
    name = file[:-4]
    img = Image.fromarray(im)
    img.save('./output_image/{}.png'.format(name))
