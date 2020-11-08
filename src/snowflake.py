#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8
import numpy as np
import matplotlib.pyplot as plt 
import cell


if __name__ == "__main__":
    # Grid later
    grid = np.genfromtxt("flaky.csv", delimiter=",")

    plt.imshow(grid)
    plt.show()
    