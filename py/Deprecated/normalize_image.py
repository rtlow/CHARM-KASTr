import numpy as np
import copy

def normalize_image(image, norm_flat, mask):
    
    norm_image = copy.deepcopy(image)
    
    nf = copy.deepcopy(norm_flat)

    m = copy.deepcopy(mask)

    for i in range(nf.shape[0]):
        for j in range(nf.shape[1]):
            if m[i][j] == 0:
                norm_image[i][j] = np.divide(norm_image[i][j], nf[i][j])


    return norm_image