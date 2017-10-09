import random
import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation

import numpy as np

#interpolate between x0 and x1
def interpolate(x0,x1,w):
    return (1 - w)*x0 + w*x1

def fade(t):
    return 6*t**5 - 15*t**4 + 10*t**3

def cantor_pairing(coord):
    x = coord[0]
    y=coord[1]
    num = 0.5*((x + y)**2 + 3*x + y)
   
    for c in coord[2:]:
        num = 0.5*((num + c)**2 + 3*num + c)%4294967279 
        
    return num

#get a normalized random gradient
def get_gradient(coord):
    #use cantor pairing function to get injectively map natural numbers to each coordinate.(enumerate them)
    
    num = cantor_pairing(coord)
    
    #seed the random number generator with the unique number.
    np.random.seed(round(num))
    
    #return a random normalized gradient
    return np.random.uniform(1,-1,len(coord)) 

    
def perlin(coord):
    #store corners vertices of the hypercube
    corners = []
    #store the dot products
    dot_products = []
    
    for i in range(2**len(coord)):
        corners.append([])
        vec = []
        
        for x in range(len(coord)):
            #floor the coordinate components.
            if coord[x]<0:
                corners[i].append(float(int(coord[x]) - 1))
            else:
                corners[i].append(float(int(coord[x])))
            #add 1 to each vector's components depending on their index.
            #i will range through from (0) to (2**(n) - 1) so changing i's binary forms
            #into a vectors will cover each point on the hypercube of n dimensions.
            #And we can use 2**x for {x:0 to (n-1)} to add to the individual components.
            if i&2**x:
                corners[i][x] += 1
            #get vector of corner to coordinate.
            vec.append(coord[x] - corners[i][x])
        
        #get dot prod of vector and it's corresponding gradient.    
        dot_products.append(np.dot(get_gradient(corners[i]),vec))
    
    #vector used for interpolation
    interpolate_vec = [fade(coord[i] - corners[0][i]) for i in range(len(coord))]
    
    interpolated_values = dot_products  
    #interpolate along each dimension.
    for dim in range(len(coord),0,-1):
        #in each dimensions here will be 2**(dim-1) interpolations.
        for i in range(2**(dim-1)):
            #interpolate along axes from largest to smallest. e.g y axis(1) then x axis(0)
            interpolated_values[i] = interpolate(interpolated_values[i], interpolated_values[i + 2**(dim-1)], interpolate_vec[dim-1])
            
    return interpolated_values[0]

#use matplotlib to plot the graph


fig = plt.figure()
ax = fig.gca(projection='3d')

l = 20
xs=np.linspace(96,97,l)
ys=np.linspace(96,97,l)

xys=np.transpose([np.tile(xs, len(ys)), np.repeat(ys, len(xs))])
z = np.zeros(l**2)
for i in range(1,8): 
    z +=  np.transpose(np.apply_along_axis(perlin,1,i*xys)*(1000/i))

ax.plot_surface(np.reshape(xys[:,0],(l,l)), np.reshape(xys[:,1],(l,l)), np.reshape(z,(l,l)),cmap=cm.coolwarm, rstride=1, cstride=1)

def animate(t):
    l = 20
    xs=np.linspace(90,91,l)
    ys=np.linspace(90,91,l) + 0.05*t
    
    
    xys=np.transpose([np.tile(xs, len(ys)), np.repeat(ys, len(xs)),np.full(l**2,0.01*t)])
    z = np.zeros(l**2)
    for i in range(1,8): 
        z +=  np.transpose(np.apply_along_axis(perlin,1,i*xys)*(1000/i))    
    
    ax.clear()
    ax.plot_surface(np.reshape(xys[:,0],(l,l)), np.reshape(xys[:,1],(l,l)), np.reshape(z,(l,l)),cmap=cm.coolwarm, rstride=1, cstride=1)
    
ani = animation.FuncAnimation(fig, animate)
plt.show()