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

def check_validity(x,y):
    if (x<=-1 or y<=-1 or x>=length or y>=width):
        return 0
    if (imap[y][x]!=0):
        return 0
    else:
        return 1

def flood_fill(x,y,color):
    '''
    This function is used to mark separated areas with different value (color)
    Param:
    x,y: coordinate of the start point
    color: initial color for the first area
    '''
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

def main(in_dir,out_dir):
    '''
    This function is used to export the output annotation mask npy file
    Param:
    - in_dir: Input folder directory
    - out_dir: Output folder directory
    '''
    for file in in_dir:
        name = file[:-4]
        imap = np.load(data_input+"/"+file)
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

        np.save(out_dir+"/"+name+".npy",imap)


if __name__ == '__main__':
    
    #Get the current directory
    os.chdir('../../../dataset/')
    main_dir = os.getcwd()
    in_folder = input("Enter input folder name here: ")
    out_folder = input("Enter output folder name here: ")
    
    #Create absolute path:
    in_dir = os.path.join(main_dir,in_folder)
    out_dir = os.path.join(main_dir,out_folder)
    main(in_dir,out_dir)