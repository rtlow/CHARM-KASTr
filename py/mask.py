import copy

import numpy as np

def mask(mflat, mbias):
    subtr = mflat - mbias

    mask = copy.deepcopy(subtr)

    for x in np.nditer(mask, op_flags=['readwrite']):
        if (x <= 10):
            x[...] = 1
        else:
            x[...] = 0
    return mask
