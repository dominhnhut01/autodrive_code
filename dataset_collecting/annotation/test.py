import numpy as np
import matplotlib.pyplot as plt
import sys
from PIL import Image
import os
sys.setrecursionlimit(25000)

imap = np.array([[0,0,1,0,2,0,1,0,0],
                 [0,0,1,0,2,0,1,0,0],
                 [1,1,1,0,2,0,1,0,0],
                 [0,0,0,0,2,0,1,1,1],
                 [2,2,2,2,2,1,0,0,0],
                 [0,0,0,0,2,1,0,0,0],
                 [1,1,0,0,2,1,0,0,0],
                 [0,1,0,0,2,1,0,0,0]])

def check_validity(x,y):
    if (x<=-1 or y<=-1 or x>=length or y>=width):
        return 0
    if (imap[y][x]!=0):
        return 0
    else:
        return 1

def flood_fill(x,y,color):
    point_queue = []
    point_queue.append((x,y))
    while (len(point_queue)!=0):
        (x1,y1) = point_queue.pop(0)
        if (check[y1][x1]==1):
            continue
        else:
            check[y1][x1]=1
            imap[y1][x1] = color
            if check_validity(x1+1,y1):
                point_queue.append((x1+1,y1))
                #print("here")
            if check_validity(x1,y1+1):
                point_queue.append((x1,y1+1))
                #print("here")
            if check_validity(x1-1,y1):
                point_queue.append((x1-1,y1))
                #print("here")
            if check_validity(x1,y1-1):
                point_queue.append((x1,y1-1))
                #print("here")
def spr2(x,y):
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
    if (x==-1 or y==-1 or x==imap.shape[1] or y==imap.shape[0]):
        return
    else:
        if (imap[y][x] not in container and (imap[y][x]!=2 and imap[y][x]!=1)):
            container.append(imap[y][x])
        return
data_input = "./street_data_np - Copy"
data_output = "./fixed_array"
#file_direc = os.listdir(data_input)



imap = np.zeros((600,600))
imap[3:4]=1
imap[200:201]=2
imap[300:301]=1
imap = np.load('E:/college_projects/autodrive_car/dataset/output_tif/NYC/street_data_np/street_data_15.npy')
length = imap.shape[1]
width = imap.shape[0]
check = np.zeros((width,length))
color = 3
container = []
for y in range(width):
    for x in range(length):
        if (imap[y][x]==0):
            flood_fill(x,y,color)
            color= color+1

for y in range(width):
    for x in range(length):
        if (imap[y][x]==2):
            spr2(x,y+1)
            spr2(x+1,y)
            spr2(x-1,y)
            spr2(x,y-1)
for y in range(width):
    for x in range(length):
        if (imap[y][x] in container or imap[y][x]==2):
            imap[y][x]=255
        else:
            imap[y][x]=0

plt.imshow(imap)
plt.show()
