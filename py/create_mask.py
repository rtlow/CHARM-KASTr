import copy

import numpy as np

from bias_subtract import bias_subtract

def create_mask(flat, bias):
    
    subtr = bias_subtract(flat, bias)
    
    mask = copy.deepcopy(subtr)
    s = copy.deepcopy(subtr)
    t = copy.deepcopy(subtr)

    medx = np.median(s, axis=0)
    medy = np.median(t, axis=1)


    for i in range(s.shape[0]):
        for j in range(s.shape[1]):
            if (medx[j] < 5000):
                s[i][j] = 1
            else:
                s[i][j] = 0

    for j in range(t.shape[1]):
        for i in range(t.shape[0]):
            if (medy[i] < 50):
                t[i][j] = 1
            else:
                t[i][j] = 0

    for i in  range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if (s[i][j] == 1 or t[i][j] == 1):
                mask[i][j] = 1

            else:
                mask[i][j] = 0

    return mask

