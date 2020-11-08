import numpy as np
import matplotlib.pyplot as plt
from plotoptix import TkOptiX,NpOptiX
from plotoptix.enums import Geometry
from plotoptix.materials import m_dispersive_glass, m_diffuse, m_matt_glass, m_mirror,m_metallic
from snowflake_tools import generate_snowflake
import math

class params():
    n = 10
    a = 5
    s = a / n
    xyz = np.mgrid[0:a:s, 0:a:s, 0:a:s].reshape(3,-1).T
    m = xyz.shape[0]
    u = np.zeros((m,3)); u[:,0] = s
    v = np.zeros((m,3)); v[:,1] = s
    w = np.zeros((m,3)); w[:,2] = s
    t = 0

def init(rt: NpOptiX) -> None: # configure data and scene at initialization
    rt.set_data("plot", pos=params.xyz, u=params.u, v=params.v, w=params.w, geom="Parallelepipeds")
    rt.set_param(min_accumulation_step=4, max_accumulation_frames=100)
    rt.setup_camera("cam1", eye=[10, 10, 10], fov=40)
    rt.setup_light("light1", color=10*np.array([0.99, 0.95, 0.91]), radius=4) # default position fits current camera
    rt.set_ambient([0.1, 0.2, 0.3]) # bluish ambient light
    rt.set_background(0)            # black background
    rt.add_postproc("Denoiser")     # denoise each frame


def compute(rt: NpOptiX, delta: int) -> None: # compute scene updates in parallel to the raytracing
    params.t += 0.02 * delta
    cost = math.cos(params.t)
    sint = math.sin(params.t)
    pia = math.pi / params.a
    for i in range(params.m):
        params.u[i] = params.s * 0.5*(1 + math.sin(pia * params.xyz[i,0] + 1.7 * params.t)) * np.array([cost, sint, 0])
        params.v[i] = params.s * 0.5*(1 + math.sin(pia * params.xyz[i,1] + 1.3 * params.t)) * np.array([-sint, cost, 0])
        params.w[i] = 0.5*(1 + math.sin(2 * pia * params.xyz[i,2] + params.t)) * np.array([0, 0, params.s])

def update_data(rt: NpOptiX) -> None:         # this is the place to update data (raytracing is finished here)
    rt.update_data("plot", u=params.u, v=params.v, w=params.w)

def update_image(rt: NpOptiX) -> None:        # update your image here
    imgplot.set_data(rt._img_rgba) # safe to read the image directly, it is locked during the callback
    plt.draw()

width = height = 500 # square 500x500 pixels
imgplot = plt.imshow(np.zeros((height, width, 4), dtype=np.uint8))
# plt.show()


optix = NpOptiX(
    on_initialization=init,
    on_scene_compute=compute,
    on_rt_completed=update_data,
    on_launch_finished=update_image,
    width=width, height=height,
    start_now=True)

optix.pause_compute()

# optix.resume_compute()
optix.close()