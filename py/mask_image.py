import numpy as np
import copy

def mask_image(image, mask):
    
    masked_image = copy.deepcopy(image)
    
    image_median = np.median(masked_image)
    
    for i in range(len(masked_image)):
        for j in range(len(masked_image[i])):
            if mask[i][j] == 1:
                masked_image[i][j] = image_median
                
                
    return masked_image