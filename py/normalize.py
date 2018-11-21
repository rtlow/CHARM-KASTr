import numpy as np

import copy

def normalize(flat, mask):

    f = copy.deepcopy(flat)

    m = copy.deepcopy(mask)

    MEDIAN = []

    for i in range(f.shape[0]):
        for j in range(f.shape[1]):
            if m[i][j] == 0:
                MEDIAN.append(f[i][j])


    median = np.median(MEDIAN)

    f = f / median


    return f

