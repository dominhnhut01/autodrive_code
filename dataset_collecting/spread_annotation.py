import numpy as np
'''
imap is the initial image changed into a numpy array
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
check[y,x] and conf[y,x] are both dynamic programming arrays used in the spr() recursive function
y,x should be the y size and x size of the original picture
'''
print (imap.shape[0]) #8
print (imap.shape[1]) #9
check = np.zeros((imap.shape[0],imap.shape[1]))
conf = np.zeros((imap.shape[0],imap.shape[1]))
'''
print(imap)
def sprder(x, y):
    if (check[x][y]== true ):
        return
    else:
        check[x][y]=true
        if (x==0 or x==n+1 or y==0 or y==n+1):
        if (imap[x][y]==0):
            if (arr[x+1][y]!=0 and arr[x][y+1]!=0 and arr[x-1][y]!=0 and arr[x][y-1]!=0):
                if (arr[x+1][y]==2 or arr[x][y+1]==2 or arr[x-1][y]==2 or arr[x][y-1]==2):
                    arr[x][y]=2
                else:
                    arr[x][y]=1
            else:
                sprder(x+1,y)
                sprder(x,y+1)
                sprder(x-1,y)
                sprder(x,y-1)
        else:
            return

dump function, don't touch this
'''

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
    if (x==-1 or y==-1 or x==imap.shape[1] or y==imap.shape[0]):
        return 1
    if (imap[y][x]!=0):
        return 1
    if (check[y][x]==0):
        check[y][x]=1
        spr(x+1,y,val)
        spr(x,y+1,val)
        spr(x-1,y,val)
        spr(x,y-1,val)
        if (spr(x+1,y,val) or spr(x,y+1,val) or spr(x,y-1,val) or spr(x-1,y,val)):
            conf[y][x]=1
            imap[y][x]=val
    else:
        return conf[y][x]

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


container=[]
global_val = 3
imap = np.load("E:/college_projects/autodrive_car/dataset/output_tif/NYC/street_data_np/street_data_20.npy")
for y in range(imap.shape[0]):
    for x in range(imap.shape[1]):
        if (imap[y][x]==0):
            spr(x,y,global_val)
            global_val= global_val+1
for y in range(imap.shape[0]):
    for x in range(imap.shape[1]):
        if (imap[y][x]==2):
            spr2(x,y+1)
            spr2(x+1,y)
            spr2(x-1,y)
            spr2(x,y-1)
for y in range(imap.shape[0]):
    for x in range(imap.shape[1]):
        if (imap[y][x] in container or imap[y][x]==2):
            imap[y][x]=255
        else:
            imap[y][x]=0
#print(imap)
#print(container)
