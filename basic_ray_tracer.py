import numpy as np
from plotoptix import TkOptiX,NpOptiX
from plotoptix.enums import Geometry
from plotoptix.materials import m_dispersive_glass, m_diffuse, m_matt_glass, m_mirror,m_metallic
from snowflake_tools import generate_snowflake

input_path="./Nice_flake/"
output_path="./Renders"
# dataname=r"full_save.npz"
# points= np.load(input_path+dataname,"r+")["arr_0"]



rad = 0.13

# points = np.load("full_save.npz","r+")["arr_0"]
# Fullpoints = np.zeros([points.shape[1],3])

# Fullpoints[:,0] = points[0,:]
# Fullpoints[:,1] = points[1,:]

plot = TkOptiX()
plot.setup_material("ice",m_metallic)
plot.set_ambient(0.7)
plot.set_background(0.4)

# plot.load_mesh_obj("./mesh/prism", "hexa")

for i in range(1,6):
    # points = np.load(input_path+str(i)+".npz","r+")["arr_0"]
    points = generate_snowflake().T

    Fullpoints = np.zeros([points.shape[1],3]) 

    Fullpoints[:,0] = points[0,:]+10*i
    Fullpoints[:,1] = points[1,:]
    # Fullpoints[:,2] = 2*i

    
    plot.set_data("flake"+str(i),Fullpoints,rad, c=[0.85,0.85,1],mat="ice",rnd=False, geom=Geometry(8))
# n = 100000                             # 1M points, better not try this with matplotlib
# xyz = 3 * (np.random.random((n, 3)) - 0.5)   # random 3D positions
# r = 0.02 * np.random.random(n) + 0.002       # random radii

# plot = TkOptiX()
# plot.set_data("my plot", xyz, r=r)
# plot.get_rt_size()
plot.show()
