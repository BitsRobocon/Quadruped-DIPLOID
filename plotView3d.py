# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 17:49:13 2020
@author: Deep

How to use:
    import plotView3d as view3d
    view3d.drawPoints3d([1,2,3])
    view3d.drawCurve3d([[1,2,2], [5,6,7]])
    view3d.drawCurve3d(p)
Refer: https://www.w3schools.com/python/python_modules.asp
"""
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# enter elevation & azimuthal angle to initialize a view
# ax.view_init(elev=20., azim=135)

def drawPoints3d(p): #to plot point(s) in 3d
    '''
    param : list of x,y,z triplets ex-[[x1,y1,z1], [x2,y2,z2], ...]
            individual point may also work
            
    returns : nothing
    '''
    p=np.array(p)
    if p.shape == (3,):
        print('You have inputted a linear list of single x,y,z')
        p=[p]
        print('changed to matrix')
    n_of_points=len(p)
    X=[]
    Y=[]
    Z=[]
    for i in range(0,n_of_points):
        # plt.plot([p[i][0]], [p[i][1]], [p[i][2]],'bo',lw=1)
        X.append(p[i][0])
        Y.append(p[i][1])
        Z.append(p[i][2])
        
    ax.scatter3D(X, Y, Z, cmap='Greens', marker='o')
    plt.show()
    return

def drawCurve3d(p): #to draw line/curve in 3d
    '''
    param : list of x,y,z triplets ex-[[x1,y1,z1], [x2,y2,z2], ...]
            individual point may also work
            
    returns : nothing
    '''
    p=np.array(p)
    if p.shape == (3,):
        print('You have inputted a linear list of single x,y,z')
        p=[p]
        print('Can\'t draw a line with one point')
    n_of_points=len(p)
    X=[]
    Y=[]
    Z=[]
    for i in range(0,n_of_points):
        X.append(p[i][0])
        Y.append(p[i][1])
        Z.append(p[i][2])
        
    ax.plot3D(X, Y, Z, 'black')
    return
