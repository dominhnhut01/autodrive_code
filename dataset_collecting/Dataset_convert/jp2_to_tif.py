import os

#direc = "./input"
#out_direc = "~/Yours/Projects/SDC/dataset/output"
direc = input("Enter input data directory here: ")
out_direc = input("Enter output data directory here: ")
for file in os.listdir(direc):
    name = file[0:-4]
    print(name)
    os.system("gdal_translate {}/{} {}/{}.tif".format(direc,file,out_direc,name))

for file in os.listdir(out_direc):
    if (file[-3:]!="tif"):
        os.remove("{}/{}".format(out_direc,file))