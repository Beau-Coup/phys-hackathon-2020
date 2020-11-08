#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8
import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt 
from numba import jit

# Defining the update rules for the simulation
@jit(nopython=True)
def edge_mask(x):
    mask = np.zeros(x.shape)
    mask[0] = 1
    mask[x.shape[0] - 1] = 1
    mask[:, 0] = 1
    mask[:, x.shape[1] - 1] = 1
    return mask

from numpy.fft import fft2, ifft2
def neighbours(y):
    """ 2D convolution, using FFT"""
    x = np.zeros(y.shape)
    M, N = y.shape
    x[M // 2-1: M // 2 +2, N // 2-1: N//2 +2] = 1
    x[M//2-1, N//2-1] = x[M//2+1, N//2+1] = 0
    fr = fft2(x)
    fr2 = fft2(np.flipud(np.fliplr(y)))
    m,n = fr.shape
    cc = np.real(ifft2(fr*fr2))
    cc = np.roll(cc, -m//2+1,axis=0)
    cc = np.roll(cc, -n//2+1,axis=1)
    return cc

@jit(nopython=True)
def get_frozen(grid):
    crystal_grid = np.zeros(grid.shape)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            crystal_grid[i, j] = 1 
    return crystal_grid

@jit
def receptive(grid):
    # Convolve to determine which cells are receptive
    crystal = get_frozen(grid)
    receptive_mask = neighbours(crystal)
    return np.clip(receptive_mask, 0, 1)


@jit(nopython=True)
def update_values(grid, receptive_grid):
    # Create the cell update parameters based 
    # on the receptive_grid
    u = (1 - receptive_grid) * grid 
    v = receptive_grid * grid

    return u, v

@jit
def update(u, v, alpha, beta, gamma):
    # This performs the update on each cell
    v += gamma

    u_bar = neighbours(u) / 7
    u += alpha / 2 * (u_bar - 8 * u / 7)

    u[0] = u[u.shape[0] - 1] = u[:, 0] = u[:, u.shape[1] - 1] = beta
    return u + v


@jit(nopython=True)
def evolution(ITERATIONS, grid):
    for i in range(ITERATIONS):
        if i % 1000 == 0:
            print(i)
        # Loop-de-loop
        rec_mask = receptive(grid)
        #plt.imshow(rec_mask)
        #plt.show()
        u, v = update_values(grid, rec_mask)

        grid = update(u, v, alpha, beta, gamma)
    return grid

if __name__ == "__main__":
    alpha = 1
    beta = 0.3
    gamma = 0.001

    N = 124
    ITERATIONS = 200
    grid = np.ones((N, N), dtype=np.float) * beta
    grid[(N-1)//2, (N-1)//2] = 1
    
    grid = evolution(ITERATIONS, grid)

    plt.imshow(get_frozen(grid))
    plt.show()
