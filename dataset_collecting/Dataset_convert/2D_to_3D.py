import numpy as np
import os 
from PIL import Image

def to_3D(in_dir):
    i=0
    for file_dir in os.listdir(in_dir):
        img= Image.open(in_dir+'/'+file_dir)
        stacked_img = np.stack((img,)*3, axis=-1)
        stacked_img=Image.fromarray(stacked_img,'RGB')
        stacked_img.save(in_dir+'/'+file_dir)
        i+=1
        if i%100==0:
        	print('Processed {} images!'.format(i))
def main():
    file_dir=input('Input your image directory: ')
    to_3D(file_dir)

if __name__ == '__main__':
    main()