import numpy as np
import copy

def extract_spectrum(image, slit_fit, weight_func):
    
    cent_slc = []
    
    for i in range(len(image[:,0])):
        slc = image[i,:]
        
        cent_slc.append(slc[ int(slit_fit(i) - 10):int(slit_fit(i) + 10)])
        
    '''    
    w_slc = []
    
    for i in range(len(cent_slc)):
        slc = cent_slc[i]
        
        smax = np.amax(slc)
        smedian = np.median(slc)
        
        slc = slc - smedian
        
        slc = np.divide(slc, smax)
        
        w_slc.append(slc)
        
    w_func = np.median(w_slc, axis=0)
    '''
    
    flx_slc = copy.deepcopy(cent_slc)
    
    w_func = copy.deepcopy(weight_func)
    
    spec = []
    
    for i in range(len(flx_slc)):
        for j in range(len(flx_slc[i])):
            
            if w_func[j] < 0.1:
                flx_slc[i][j] = flx_slc[i][j] - np.median(flx_slc[i])
                
            flx_slc[i][j] = flx_slc[i][j] * w_func[j]
            
        spec.append(np.divide(np.sum(flx_slc[i]), np.sum(w_func)))
        
    return spec
        
   
        
        
    