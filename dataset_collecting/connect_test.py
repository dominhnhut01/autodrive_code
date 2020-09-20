import numpy as np
import matplotlib.pyplot as plt
import math
import sys

'''
img = np.array([[0,0,1,0,0,0,0,0,1,0,0],
            	[0,0,0,0,0,0,0,0,0,0,0],
            	[0,0,0,1,0,0,0,0,1,0,0],
           		[0,0,0,0,0,0,0,1,0,0,0],
            	[0,0,0,1,0,0,0,1,0,0,0],
            	[0,0,0,0,0,0,0,1,0,0,0],
            	[0,0,1,0,0,0,0,0,0,0,0]])
'''

class Black_Points:
	def __init__(self,img):
		self.img = img
		self.check=0
		self.visited = np.array([])
		self.black_point_list = np.where(img==1)
		self.non_visited = np.zeros([np.shape(self.black_point_list)[1],2],int)
		for i in range(len(self.black_point_list[0])):
			self.non_visited[i][0] = self.black_point_list[0][i]
			self.non_visited[i][1] = self.black_point_list[1][i]
	

	def add_visited(self,new_point):
		np.append((self.visited,new_point))
	

	def pop_non_visited(self,start_point):
		temp_coor = np.where(np.all(self.non_visited== start_point, axis=1))
		self.non_visited = np.delete(self.non_visited,temp_coor,0)
		if len(self.non_visited)==0:
			print("first_point: ", self.first_point)
			print("len(non_visited): ",len(self.non_visited))
			self.non_visited = np.array([self.first_point]) 
			self.check+=1
		print("non_visited: ",self.non_visited)


	def add_queue(self, new_point):
		self.queue = np.append(self.queue,new_point)
	

	def find_next_point(self,start_point):
		self.pop_non_visited(start_point)
		min_dist = int(sys.maxsize)
		for point in self.non_visited:
			dist = math.sqrt((point[0]-start_point[0])**2+(point[1]-start_point[1])**2)
			if dist < min_dist:
				min_dist=dist
				next_point=point
		print("Min dist: ",min_dist)
		print("Start point: ",start_point)
		print("Next point: ",next_point)
		return next_point

	
	def connect(self,start_point,next_point):
		y_dist = next_point[0]-start_point[0]
		x_dist = next_point[1]-start_point[1]
		print("y_dist, x_dist:",y_dist,x_dist)
		if y_dist>=0:
			for y in range(y_dist+1):
				coor = np.array([start_point[0]+y,start_point[1]])
				img[coor[0],coor[1]] = 1
				print(img)
		if y_dist<0:
			for y in range(0,y_dist-1,-1):
				coor = np.array([start_point[0]+y,start_point[1]])
				img[coor[0],coor[1]] = 1
				print(img)
		if x_dist>=0:
			for x in range(x_dist+1):
				coor = np.array([start_point[0]+y_dist,start_point[1]+x])
				img[coor[0],coor[1]] = 1
				print(img)
		if x_dist<0:	
			for x in range(0,x_dist-1,-1):
				coor = np.array([start_point[0]+y_dist,start_point[1]+x])
				img[coor[0],coor[1]] = 1
				print(img)
	def travel(self):
		i=0
		print(self.non_visited)
		start_point = self.non_visited[0]
		self.first_point = self.non_visited[0]
		while len(self.non_visited)!=0 and self.check<2:
			next_point = self.find_next_point(start_point)
			self.connect(start_point,next_point) 
			start_point = next_point           
			i+=1
			print('i',i)
			print(img)


img= np.load("E:/college_projects/autodrive_car/dataset/output_tif/NYC/street_data_np/street_data_20.npy")
#obj = Black_Points(img)
#obj.travel()
plt.imshow(img)
plt.show()
