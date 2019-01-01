import numpy as np
import copy

def normalize_image(image, norm_flat):
    
    norm_image = copy.deepcopy(image)
    
    norm_image = np.divide(norm_image, norm_flat)
        
    return norm_image