import numpy as np
import matplotlib.pyplot as plt
import math

class Black_Points(img):
	def __init__(self):
		self.img = img
		self.init_point = np.where(img==1)
		self.visited = np.array([])
	def add_visited(self,new_point):
		np.append((self.visited,new_point))
	def pop_init_point(self,deleted_point):
		self.init_point = np.delete(self.init_point,deleted_point)
	def find_next_point(self,start_point):
		self.dist_dict = {} #key: coordinate, value: distance
		for point in np.delete(self.init_point,start_point):
			dist = math.sqrt((point[0]-start_point[0])**2+(point[1]-start_point[1])**2)
			dist_dict[dist]=point
		dist_list = np.fromiter(dist_dict.keys(), dtype=float)
		min_dist = np.amin(dist_list)
		return dist_dict[min_dist]
	def connect(self,start_point,next_point):
		y_dist = abs(start_point[0]-next_point[0])
	    x_dist = abs(start_point[1]-next_point[1])
	    for y in range(y_dist+1):
	        for x in range(x_dist+1):
	            coor = [start_point[0]-y,start_point[1]-x]
	            img[coor[0],coor[1]] = 1
