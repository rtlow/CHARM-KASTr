import numpy as np
import copy

def extract_variance(var_image, slit_fit, weight_func):
    
    cent_slc = []
    
    for i in range(len(var_image[:,0])):
        slc = var_image[i,:]
        
        cent_slc.append(slc[ int(slit_fit(i) - 10):int(slit_fit(i) + 10)])
        
    
    var_slc = copy.deepcopy(cent_slc)
    
    w_func = copy.deepcopy(weight_func)
    
    variance = []
    
    for i in range(len(var_slc)):
        for j in range(len(var_slc[i])):
            var_slc[i][j] = var_slc[i][j] * w_func[j]
            
        variance.append(np.divide(np.sum(var_slc[i]), np.sum(w_func)))
        
    return variance