import numpy as np
from plotoptix import TkOptiX
from plotoptix.enums import Geometry



rad = 0.2

points = np.load("full_save.npz","r+")["arr_0"]
Fullpoints = np.zeros([points.shape[1],3])

Fullpoints[:,0] = points[0,:]
Fullpoints[:,1] = points[1,:]

plot = TkOptiX()
plot.set_data("myplot",Fullpoints,rad, c=[0.7,0.7,1])#, geom=Geometry(8))
# n = 100000                             # 1M points, better not try this with matplotlib
# xyz = 3 * (np.random.random((n, 3)) - 0.5)   # random 3D positions
# r = 0.02 * np.random.random(n) + 0.002       # random radii

# plot = TkOptiX()
# plot.set_data("my plot", xyz, r=r)
# plot.get_rt_size()
plot.show()
