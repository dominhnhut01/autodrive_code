import numpy as np
import matplotlib.pyplot as pyplot
import sys
from PIL import Image
import os
sys.setrecursionlimit(25000)
'''
imap = np.array([[0,0,1,0,2,0,1,0,0],
                 [0,0,1,0,2,0,1,0,0],
                 [1,1,1,0,2,0,1,0,0],
                 [0,0,0,0,2,0,1,1,1],
                 [2,2,2,2,2,1,0,0,0],
                 [0,0,0,0,2,1,0,0,0],
                 [1,1,0,0,2,1,0,0,0],
                 [0,1,0,0,2,1,0,0,0]])
'''
class RoadData:
    def __init__(self,in_direc,out_direc):
        self.name=os.path.basename(in_direc)[:-4]
        self.out_direc=out_direc
        self.imap=np.load(in_direc)
        self.length=self.imap.shape[1]
        self.width=self.imap.shape[0]
        print(self.width,self.length)
        self.check=np.zeros((self.width,self.length))
        self.color=3
        self.container=[]
    def check_validity(self,x,y):
        if (x<=-1 or y<=-1 or x>=self.length or y>=self.width):
            return 0
        if (self.imap[y][x]!=0):
            return 0
        else:
            return 1
    def flood_fill(self,x,y):
        point_queue = []
        point_queue.append((x,y))
        while (len(point_queue)!=0):
            (x1,y1) = point_queue.pop(0)
            if (self.check[y1][x1]==1):
                continue
            else:
                self.check[y1][x1]=1
                self.imap[y1][x1] = self.color
                if self.check_validity(x1+1,y1):
                    point_queue.append((x1+1,y1))
                    #print("here")
                if self.check_validity(x1,y1+1):
                    point_queue.append((x1,y1+1))
                    #print("here")
                if self.check_validity(x1-1,y1):
                    point_queue.append((x1-1,y1))
                    #print("here")
                if self.check_validity(x1,y1-1):
                    point_queue.append((x1,y1-1))
                    #print("here")
    
    def spr2(self,x,y):
        '''
        doesn't return anything
        spr2 just checks which sections border with the street's center line and add those sections into a list
        params:
        x,y is the index of the element
        EX:
        3 1 4 2 5
        1 1 4 2 5
        4 4 4 2 5
        2 2 2 2 5
        spr2()
        OUT:
        container= [4,5]
        '''
        if (x==-1 or y==-1 or x==self.imap.shape[1] or y==self.imap.shape[0]):
            return
        else:
            if (self.imap[y][x] not in self.container and (self.imap[y][x]!=2 and self.imap[y][x]!=1)):
                self.container.append(self.imap[y][x])
            return
    def run(self):
        for y in range(self.width):
            for x in range(self.length):
                if (self.imap[y][x]==0):
                    self.flood_fill(x,y)
                    self.color= self.color+1

        for y in range(self.width):
            for x in range(self.length):
                if (self.imap[y][x]==2):
                    self.spr2(x,y+1)
                    self.spr2(x+1,y)
                    self.spr2(x-1,y)
                    self.spr2(x,y-1)
        for y in range(self.width):
            for x in range(self.length):
                if (self.imap[y][x] in self.container or self.imap[y][x]==2):
                    self.imap[y][x]=255
                else:
                    self.imap[y][x]=0

        np.save(self.out_direc+"/"+self.name+".npy",self.imap)
        print('Exported {}.npy'.format(self.name))

def file_iteration(in_direc,out_direc):
    for file_name in os.listdir(in_direc):
        file_direc='{}/{}'.format(in_direc,file_name)
        RoadDataFile=RoadData(file_direc,out_direc)
        RoadDataFile.run()


if __name__=='__main__':
    #Get the current directory
    os.chdir('../../../dataset/')
    main_direc = os.getcwd()
    in_folder = input("Enter input folder name here: ")
    out_folder = input("Enter output folder name here: ")
    
    #Create absolute path:
    in_direc = os.path.join(main_direc,in_folder)
    out_direc = os.path.join(main_direc,out_folder)
    file_iteration(in_direc,out_direc)

