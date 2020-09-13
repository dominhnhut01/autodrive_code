import numpy as np
import os
import sys
sys.setrecursionlimit(25000)

imap = np.array([[0,0,1,0,2,0,1,0,0],
                 [0,0,1,0,2,0,1,0,0],
                 [1,1,1,0,2,0,1,0,0],
                 [0,0,0,0,2,0,1,1,1],
                 [2,2,2,2,2,1,0,0,0],
                 [0,0,0,0,2,1,0,0,0],
                 [1,1,0,0,2,1,0,0,0],
                 [0,1,0,0,2,1,0,0,0]])
visited = []
length = imap.shape[1]
width = imap.shape[0]
def neighbours(r, c):
    """Calculates the neighbours of a given cell"""
    return [[r+1, c], [r, c+1], [r-1, c], [r, c-1]]
def spr(x,y,val):
    '''
    spr(x,y,val) is a recursive function used to divide each non-bordering section into a seperate value
    EX: 0 1 0 2 0
        1 1 0 2 0
        0 0 0 2 0
        2 2 2 2 0
    for:
        for:
            spr(x,y,global_val)
            global_val++
    OUT:
        3 1 4 2 5
        1 1 4 2 5
        4 4 4 2 5
        2 2 2 2 5
    params:
    x, y is the index of the element in the array
    val is the value being held (index of the section)
    '''
    if (x<=-1 or y<=-1 or x>=length or y>=width):
        return
    if (imap[y][x]!=0):
        return

    imap[y][x]=val
    visited.append([y,x])
    moves = neighbours(y,x)
    for move in moves:
        if move not in visited:
            spr(move[0], move[1], val)
    '''
    if (check[y][x]==0):
        check[y][x]=1
        spr(x+1,y,val)
        spr(x,y+1,val)
        spr(x-1,y,val)
        spr(x,y-1,val)
        #if (conf[y][x+1] or conf[y+1][x] or conf[y-1][x] or conf[y][x-1]):
        #if (spr(x+1,y,val) or spr(x,y+1,val) or spr(x,y-1,val) or spr(x-1,y,val)):
        imap[y][x]=val
    else:
        return
    '''
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
file_direc = os.listdir(data_input)
for file in file_direc:
    name = file[:-4]
    imap=0
    imap = np.load(data_input+"/"+file)
    visited = []
    length = imap.shape[1]
    width = imap.shape[0]
    print (imap.shape[0]) #8
    print (imap.shape[1]) #9
    #print(imap)
    #check = np.zeros((imap.shape[0],imap.shape[1]))
    container=[]
    global_val = 3
    for y in range(imap.shape[0]):
        for x in range(imap.shape[1]):
            if (imap[y][x]==0):
                spr(x,y,global_val)
                global_val= global_val+1
    print("here1")
    for y in range(imap.shape[0]):
        for x in range(imap.shape[1]):
            if (imap[y][x]==2):
                spr2(x,y+1)
                spr2(x+1,y)
                spr2(x-1,y)
                spr2(x,y-1)
    print("here2")
    for y in range(imap.shape[0]):
        for x in range(imap.shape[1]):
            if (imap[y][x] in container or imap[y][x]==2):
                imap[y][x]=255
            else:
                imap[y][x]=0
    np.save(data_output+"/"+name,imap)
    #print(imap)
    #print(container)
    print('Done')
