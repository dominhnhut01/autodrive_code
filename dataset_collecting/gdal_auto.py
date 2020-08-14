import os
import numpy as np
#direc is directory for input dataset folder 
direc = input("Input your input directory: ")
#out_direc is directory for output folder
out_direc = input("Input your output directory: ")
num = 1
for fil in os.listdir(direc):
    name = fil[4:-4]
    print(name)
    os.system("gdal_translate -of JPEG -scale -co worldfile=yes ./input/{} {}/{}.jpg".format(fil,out_direc,name))
    num = num+1

num_del = 1
for fil in os.listdir("./output"):
    if (fil[-3:]!="jpg"):
        os.system("rm -r ./output/{}".format(fil))


