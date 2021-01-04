import cv2
import os
import numpy as np
from skimage.transform import resize
from skimage import img_as_bool

class CV2_IMAGE:
	def __init__(self,img_path):
		self.img = cv2.imread(img_path)
		self.init_height=self.img.shape[0]
		self.init_width=self.img.shape[1]
	def convert_2_grayscale(self):
		self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
	def img_resize(self):
		#Rotate the image so we can minimize the distortion when resizing
		if self.init_height<self.init_width:
			self.img_gray=cv2.rotate(self.img_gray,cv2.ROTATE_90_CLOCKWISE)
		
		self.out_img=cv2.resize(self.img_gray,(220,436))
		#cv2.imwrite('E:/college_projects/autodrive_car/autodrive_code/road_segmentation_model/models/research/deeplab/temp_img/temp.png',self.out_img)
	def run(self):
		self.convert_2_grayscale()
		self.img_resize()
		return self.out_img

def reverse_to_init(np_img,init_height,init_width,type):
	#Rotate the image back to its initial state
	#Return numpy array of the image
	if init_height>init_width:
		np_img=cv2.rotate(np_img,cv2.ROTATE_90_COUNTERCLOCKWISE)		
	
	height=np.shape(np_img)[0]
	width=np.shape(np_img)[1]
	
	if type=='binary':
		np_img= cv2.resize(np_img,(init_height,init_width),interpolation=cv2.INTER_NEAREST)
	
	if type=='grayscale':
		np_img= cv2.resize(np_img,(init_height,init_width))
	
	if type!='binary' and type!='grayscale':
		return -1
	return np_img