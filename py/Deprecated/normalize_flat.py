import numpy as np

import copy

def normalize_flat(flat, mask):

    f = copy.deepcopy(flat)

    m = copy.deepcopy(mask)

    GOOD_PIXELS = []

    for i in range(f.shape[0]):
        for j in range(f.shape[1]):
            if m[i][j] == 0:
                GOOD_PIXELS.append(f[i][j])


    median = np.median(GOOD_PIXELS)
    
    maximum = np.amax(GOOD_PIXELS)

    f = np.divide(f, median)

    return f

