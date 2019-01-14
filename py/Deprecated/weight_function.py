import numpy as np
import copy

def weight_function(image, slit_fit):
    
    cent_slc = []
    
    for i in range(len(image[:,0])):
        slc = image[i,:]
        
        cent_slc.append(slc[ int(slit_fit(i) - 10):int(slit_fit(i) + 10)])
            
    w_slc = []
    
    for i in range(len(cent_slc)):
        slc = cent_slc[i]
        
        smax = np.amax(slc)
        smedian = np.median(slc)
        
        slc = slc - smedian
        
        slc = np.divide(slc, smax)
        
        w_slc.append(slc)
        
    w_func = np.median(w_slc, axis=0)
    
    return w_func
    