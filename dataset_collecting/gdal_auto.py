import os

#direc = "./input"
#out_direc = "~/Yours/Projects/SDC/dataset/output"
direc = input("Enter input data directory here: ")
out_direc = input("Enter output data directory here: ")
num = 1

for file in os.listdir(direc):
    name = file[4:-4]
    print(name)
    print("gdal_translate -of JPEG -scale -co worldfile=yes {}/{} {}/{}.jpg".format(direc,file,out_direc,name))
    os.system("gdal_translate -of JPEG -scale -co worldfile=yes {}/{} {}/{}.jpg".format(direc,file,out_direc,name))
    num+=1

for file in os.listdir(out_direc):
    if (file[-3:]!="jpg"):
        os.system("rm -r {}/{}".format(out_direc,file))



