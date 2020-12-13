import numpy as np
import os
import matplotlib.pyplot as plt

def del_invalid(in_dir,out_dir,points):
	#This function is used to delete possible invalid annotation masks, which are almost black or almost white
	for file in os.listdir(in_dir):
	    try:
	        imap = np.load(in_dir+"/"+file)
	        registered_point = np.count_nonzero(imap == 255)
	        ratio = registered_point/imap.size
	        points.append(ratio)
	        if (ratio>0.01 and ratio<=0.7):
	            np.save(out_dir+"/"+file,imap)
	    except:
	        continue
def visualize(points):
	#This function is used to visualize the initial pixel distribution in the dataset
	x = points
	x.sort()
	range(len(x))
	range(len(points))
	plt.scatter(range(len(points)),x)
	plt.show()

if __name__ == '__main__':
	
	points = []

	#Get the current directory
	os.chdir('../../../dataset/')
	main_dir = os.getcwd()
	in_folder = input("Enter input folder name here: ")
	out_folder = input("Enter output folder name here: ")
	
	#Create absolute path:
	in_dir = os.path.join(main_dir,in_folder)
	out_dir = os.path.join(main_dir,out_folder)
	del_invalid(in_dir,out_dir,points)
	#visualize(points) 
