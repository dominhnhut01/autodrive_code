import numpy as np
import skimage.graph
from PIL import Image

from skimage.morphology import skeletonize
#import matplotlib.pyplot as plt
import numpy as np
import cv2

def dijksar(prediction_mask,start_point,end_point):
	'''
	Parameters:
	- prediction_mask: a Numpy object containing the segmentation result from the model
	- start_point: a tuple of x and y coordinates of your start point
	- end_point: a tuple of x and y coordinates of your end point
	Return:
	- skeleton: the numpy object of the skeleton image of the segmentation path
	- shortest_path: the numpy object of the shortest path
	'''


	skeleton = skeletonize(prediction_mask,method='lee')
	#source = np.where(skeleton[435]==True)
	size=skeleton.shape
	costs = np.where(skeleton, 1, 1000)
	path, cost = skimage.graph.route_through_array(
	    costs, start=start_point, end=end_point, fully_connected=True)
	shortest_path = np.zeros(size)
	for i in range(len(path)) :
	    shortest_path[path[i][0],path[i][1]]=1

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	shortest_path = cv2.dilate(shortest_path,kernel,iterations=3)
	return skeleton,shortest_path

def visualization(img,prediction_mask,skeleton,shortest_path):
	'''
	This function is used to show the result locally. Only used for testing
	'''

	fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(8, 4),
	                         sharex=False, sharey=False)

	ax = axes.ravel()

	ax[0].imshow(img)
	ax[0].axis('off')
	ax[0].set_title('image', fontsize=20)

	ax[1].imshow(prediction_mask, cmap=plt.cm.gray)
	ax[1].axis('off')
	ax[1].set_title('original', fontsize=20)

	ax[2].imshow(skeleton, cmap=plt.cm.gray)
	ax[2].axis('off')
	ax[2].set_title('skeleton', fontsize=20)

	ax[3].imshow(shortest_path, cmap=plt.cm.gray)
	ax[3].axis('off')
	ax[3].set_title('shortest_path', fontsize=20)

	fig.tight_layout()
	plt.show()


def test():
	mask= np.load('E:/college_projects/autodrive_car/autodrive_code/deployment/templates/temp_img/seg_map_npy_89L.npy')

	skeleton,shortest_path = dijksar(mask,(98,391),(133,169))

	#img = Image.open('E:/college_projects/autodrive_car/autodrive_code/deployment/templates/temp_img/seg_map_89L.jpg')
	visualization(mask, mask, skeleton, shortest_path)

if __name__ == "__main__":
	test()
