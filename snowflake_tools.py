import numpy as np

def cost(grid, pt):
    dist = 0.35
    N_ind = np.argwhere(np.abs(grid - pt) < dist)
    N = N_ind.size
    if N==0:
        return 0
    if N==1:
        return 0.1
    if N >10:
        return np.exp(-1 *N)
    
    points = grid[N_ind]
    points_x  = np.real(points)
    points_y = np.imag(points)

    pt_x = np.real(pt)
    pt_y = np.imag(pt)

    _, res = np.polyfit(np.append(points_x, pt_x), np.append(points_y, pt_y), 1)
    return min(1, 1 /np.abs(res) *(1/np.sqrt(N)) * 0.5)

def generate_snowflake(sliver_bounds = [3,8], start_points=7, n_itter=5000, spawn_spread = 0.5, spawn_reach = 1.8):
    n_slivers = np.random.choice(list(range(sliver_bounds[0], sliver_bounds[1])))
    n_start = start_points
    angles = (np.random.random_sample(n_start)*2*np.pi / (n_slivers *2))
    mag = np.sort(np.random.random_sample(n_start))
    staring_grid = mag*np.exp(1j*angles)

    



    niter = n_itter
    angles = np.random.random_sample(niter)*2*np.pi / (n_slivers *2)

    grid = staring_grid.copy()

    #plt.scatter(np.real(grid), np.imag(grid))

    for i in range(niter):

        
        far_point = np.mean(np.abs(grid)) + spawn_reach*np.std(np.abs(grid))
        variance = far_point * spawn_spread
        mag = np.random.random_sample(2) 
        possible_point = (((mag[0] - 0.5) *variance + far_point*0.7)* np.exp(1j*angles[i]))

        prob = cost(grid, possible_point)
        if mag[1]< prob:
            #aacept new point
            grid = np.append(grid, possible_point)
            #plt.scatter(np.real(possible_point), np.imag(possible_point))

        
    full_grid = np.append(grid, np.conj(grid))
    full_map =[]
    for ang in range(n_slivers):
        quad = [np.real(full_grid * np.exp(1j*2*np.pi * ang / n_slivers)), np.imag(full_grid * np.exp(1j*2*np.pi * ang / n_slivers))]
        full_map.append(quad)

    full_map = np.hstack(np.array(full_map))
    return full_map.T

if __name__=="__main__":
    import matplotlib.pyplot as plt
    flake = generate_snowflake()
    np.savez("full_save", flake)
    plt.clf()
    plt.scatter(flake[:,0], flake[:,1], s=0.2, color = "blue")
    plt.savefig("hello.png")