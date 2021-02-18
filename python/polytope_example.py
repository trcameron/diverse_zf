# polytope example
from numpy import arange, meshgrid
import matplotlib.pyplot as plt

f1 = lambda x,y : x + 4*y -1
f2 = lambda x,y : 1 - 2*x - 2*y
f3 = lambda x,y : (x - x) + (y - y)
x, y = meshgrid(arange(0,1+1E-2,1E-2),arange(0,1+1E-2,1E-2))

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_zlim3d(0,1)
ax.contour3D(x, y, f1(x,y), 75, cmap='binary')
ax.contour3D(x, y, f2(x,y), 75, cmap='binary')
ax.scatter(1/3,1/6,0,s=75,c='pink')
plt.show()