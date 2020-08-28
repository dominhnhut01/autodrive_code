import numpy as np

class region_divide:
    def __init__(self, region_coor, returned_size):
        #Enter the initial region's coordinate and returned size(width in longtitude and height in latitude)
        self.region_coor = region_coor
        self.returned_size = returned_size
        self.rescaled_region = np.zeros(4)

    def rescale(self):
        #Rescale the region coordinates
        self.rescaled_width = ((self.region_coor[2]-self.region_coor[0])//self.returned_size[0])*self.returned_size[0]
        self.rescaled_height = ((self.region_coor[3]-self.region_coor[1])//self.returned_size[1])*self.returned_size[1]
        
        #Ensure height and width are positive
        if self.rescaled_height<0:
            self.rescaled_height=-self.rescaled_height
        if self.rescaled_width<0:
            self.rescaled_width=-self.rescaled_width
        
        #Append new coordinates to the list
        self.rescaled_region[0] = self.region_coor[0]
        self.rescaled_region[1] = self.region_coor[1]
        self.rescaled_region[2] = self.region_coor[0]+self.rescaled_width
        self.rescaled_region[3] = self.region_coor[1]+self.rescaled_height

    def divide(self):
        #Divide the initial region's into smaller one. Return a np.array of coordinates of small regions
        self.rescale()
        column = int(self.rescaled_width//self.returned_size[0]) #number of column
        row = int(self.rescaled_height//self.returned_size[1]) #number of row
        self.divided_region = np.zeros((row*column,4))
        coor_num = 0
        for y in range(row):
            for x in range(column):
                self.divided_region[coor_num][0] = self.rescaled_region[0] + self.returned_size[0]*x
                self.divided_region[coor_num][1] = self.rescaled_region[1] + self.returned_size[1]*y
                self.divided_region[coor_num][2] = self.rescaled_region[0] + self.returned_size[0]*(x+1)
                self.divided_region[coor_num][3] = self.rescaled_region[1] + self.returned_size[1]*(y+1)   
                print('{} rows {} columns'.format(y+1,x+1))
                coor_num +=1
        return self.divided_region
