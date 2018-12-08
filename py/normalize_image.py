import numpy as np
import copy

def normalize_image(image, norm_flat):
    
    norm_image = copy.deepcopy(image)
    
    norm_image = norm_image / np.amax(norm_flat)
        
    return norm_image