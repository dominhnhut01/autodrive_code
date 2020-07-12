import numpy as np

class region_divide:
	def __init__(self, region_coor, returned_size):
		#Enter the initial region's coordinate and returned size(width in longtitude and height in latitude)
		self.region_coor = region_coor
		self.returned_size = returned_size

	def rescale(self):
		#Rescale the region coordinates
		self.rescaled_width = ((self.region_coor[1][0]-self.region_coor[0][0])//self.returned_size[0])*self.returned_size[0]
		self.rescaled_height = ((self.region_coor[3][1]-self.region_coor[0][1])//self.returned_size[1])*self.returned_size[1]
		#Assume the rescaled region is an rectangle ABCD
		a = [self.region_coor[0][0], self.region_coor[0][1]]
		b = [(self.region_coor[0][0]+self.rescaled_width),self.region_coor[0][1]]
		c = [(self.region_coor[0][0]+self.rescaled_width),(self.region_coor[0][1]+self.rescaled_height)]
		d = [self.region_coor[0][0],(self.region_coor[0][1]+self.rescaled_height)]
		self.rescaled_region = [a,b,c,d]
		return self.rescaled_region

	def divide(self):
		#Divide the initial region's into smaller one. Return a np.array of coordinates of small regions
		self.rescale()
		column = self.rescaled_width//self.returned_size[0] #number of column
		row = self.rescaled_height//self.returned_size[1] #number of row
		
		self.divided_region = np.zeros(row,column,4,2)
		for y in range(row):
			for x in range(column):
				#Vertex A of each small region:
				self.divided_region[y][x][0][0] = self.rescaled_region[0][0] + self.rescaled_width*x
				self.divided_region[y][x][0][1] = self.rescaled_region[0][1] + self.rescaled_height*y
				
				#Vertex B of each small region:
				self.divided_region[y][x][1][0] = self.rescaled_region[1][0] + self.rescaled_width*(x+1)
				self.divided_region[y][x][1][1] = self.rescaled_region[1][1] + self.rescaled_height*y
				
				#Vertex C of each small region:
				self.divided_region[y][x][2][0] = self.rescaled_region[2][0] + self.rescaled_width*(x+1)
				self.divided_region[y][x][2][1] = self.rescaled_region[2][1] + self.rescaled_height*(y+1)
				
				#Vertex D of each small region:
				self.divided_region[y][x][3][0] = self.rescaled_region[3][0] + self.rescaled_width*x
				self.divided_region[y][x][3][1] = self.rescaled_region[3][1] + self.rescaled_height*(y+1)

		return self.divided_region











