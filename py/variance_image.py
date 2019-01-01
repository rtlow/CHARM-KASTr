import numpy as np
import copy

#gains are in units [e-/DN]
gain_slow = 1.9

gain_fast = 0.55

#Shane KAST red read noise are in units [e-]
read_noise_slow = 3.8

read_noise_fast = 4.3


def variance_image( image ):
    var_img = copy.deepcopy(image)

    with np.nditer(var_img, op_flags=['readwrite']) as it:
        for x in it:
            x[...] = ( (np.divide(x,gain_slow)) + np.power(read_noise_slow, 2) ) * (np.power( gain_slow, 2 ))

    return var_img
