import os
import numpy as np


#direc = "./input"
#out_direc = "~/Yours/Projects/SDC/dataset/output"
direc = input("Enter input data directory here: ")
out_direc = input("Enter output data directory here: ")
num = 1
for fil in os.listdir(direc):
    name = fil[4:-4]
    print(name)
    os.system("gdal_translate -of JPEG -scale -co worldfile=yes {}/{} {}/{}.jpg".format(direc,fil,out_direc,name))
    num = num+1

num_del = 1
for fil in os.listdir("{}".format(out_direc)):
    if (fil[-3:]!="jpg"):
        os.system("rm -r {}/{}".format(out_direc,fil))


