{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'\\nimap = np.array([[0,0,1,0,2,0,1,0,0],\\n                 [0,0,1,0,2,0,1,0,0],\\n                 [1,1,1,0,2,0,1,0,0],\\n                 [0,0,0,0,2,0,1,1,1],\\n                 [2,2,2,2,2,1,0,0,0],\\n                 [0,0,0,0,2,1,0,0,0],\\n                 [1,1,0,0,2,1,0,0,0],\\n                 [0,1,0,0,2,1,0,0,0]])\\n'"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import numpy as np\n",
    "import os\n",
    "import sys\n",
    "import threading\n",
    "import matplotlib.pyplot as plt\n",
    "#threading.stack_size(0x500000)\n",
    "#print (sys.getrecursionlimit())\n",
    "sys.setrecursionlimit(3000000)\n",
    "#print (sys.getrecursionlimit())\n",
    "'''\n",
    "imap = np.array([[0,0,1,0,2,0,1,0,0],\n",
    "                 [0,0,1,0,2,0,1,0,0],\n",
    "                 [1,1,1,0,2,0,1,0,0],\n",
    "                 [0,0,0,0,2,0,1,1,1],\n",
    "                 [2,2,2,2,2,1,0,0,0],\n",
    "                 [0,0,0,0,2,1,0,0,0],\n",
    "                 [1,1,0,0,2,1,0,0,0],\n",
    "                 [0,1,0,0,2,1,0,0,0]])\n",
    "'''\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "visited = []\n",
    "\n",
    "def neighbours(r, c):\n",
    "    \"\"\"Calculates the neighbours of a given cell\"\"\"\n",
    "    return [[r+1, c], [r, c+1], [r-1, c], [r, c-1]]\n",
    "def spr(x,y,val):\n",
    "    '''\n",
    "    spr(x,y,val) is a recursive function used to divide each non-bordering section into a seperate value\n",
    "    EX: 0 1 0 2 0\n",
    "        1 1 0 2 0\n",
    "        0 0 0 2 0\n",
    "        2 2 2 2 0\n",
    "    for:\n",
    "        for:\n",
    "            spr(x,y,global_val)\n",
    "            global_val++\n",
    "    OUT:\n",
    "        3 1 4 2 5\n",
    "        1 1 4 2 5\n",
    "        4 4 4 2 5\n",
    "        2 2 2 2 5\n",
    "    params:\n",
    "    x, y is the index of the element in the array\n",
    "    val is the value being held (index of the section)\n",
    "    '''\n",
    "    \n",
    "    if (x<=-1 or y<=-1 or x>=length or y>=width):\n",
    "        return\n",
    "    if (imap[y][x]!=0):\n",
    "        return\n",
    "    '''\n",
    "    imap[y][x]=val\n",
    "    visited.append([y,x])\n",
    "    moves = neighbours(y,x)\n",
    "    for move in moves:\n",
    "        if move not in visited:\n",
    "            spr(move[0], move[1], val)\n",
    "    '''\n",
    "    if (check[y][x]==0):\n",
    "        check[y][x]=1\n",
    "        spr(x+1,y,val)\n",
    "        spr(x,y+1,val)\n",
    "        spr(x-1,y,val)\n",
    "        spr(x,y-1,val)\n",
    "        #if (conf[y][x+1] or conf[y+1][x] or conf[y-1][x] or conf[y][x-1]):\n",
    "        #if (spr(x+1,y,val) or spr(x,y+1,val) or spr(x,y-1,val) or spr(x-1,y,val)):\n",
    "        imap[y][x]=val\n",
    "    else:\n",
    "        return\n",
    "        \n",
    "def spr2(x,y):\n",
    "    '''\n",
    "    doesn't return anything\n",
    "    spr2 just checks which sections border with the street's center line and add those sections into a list\n",
    "\n",
    "    params:\n",
    "    x,y is the index of the element\n",
    "\n",
    "    EX:\n",
    "    3 1 4 2 5\n",
    "    1 1 4 2 5\n",
    "    4 4 4 2 5\n",
    "    2 2 2 2 5\n",
    "    spr2()\n",
    "    OUT:\n",
    "    container= [4,5]\n",
    "    '''\n",
    "    if (x==-1 or y==-1 or x==imap.shape[1] or y==imap.shape[0]):\n",
    "        return\n",
    "    else:\n",
    "        if (imap[y][x] not in container and (imap[y][x]!=2 and imap[y][x]!=1)):\n",
    "            container.append(imap[y][x])\n",
    "        return"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.image.AxesImage at 0x7fe5f3430a10>"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "data_input = \"./street_data_np - Copy\"\n",
    "data_output = \"./fixed_array\"\n",
    "#imap = np.zeros((200,200))\n",
    "imap = np.load(data_input+\"/street_data_1.npy\")\n",
    "length = imap.shape[1]\n",
    "width = imap.shape[0]\n",
    "plt.imshow(imap)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "check = np.zeros((width,length))\n",
    "container=[]\n",
    "global_val = 3\n",
    "for y in range(width):\n",
    "    for x in range(length):\n",
    "        if (imap[y][x]==0):\n",
    "            spr(x,y,global_val)\n",
    "            global_val= global_val+1\n",
    "for y in range(width):\n",
    "    for x in range(length):\n",
    "        if (imap[y][x]==2):\n",
    "            spr2(x,y+1)\n",
    "            spr2(x+1,y)\n",
    "            spr2(x-1,y)\n",
    "            spr2(x,y-1)\n",
    "for y in range(width):\n",
    "    for x in range(length):\n",
    "        if (imap[y][x] in container or imap[y][x]==2):\n",
    "            imap[y][x]=255\n",
    "        else:\n",
    "            imap[y][x]=0\n",
    "plt.imshow(imap)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
