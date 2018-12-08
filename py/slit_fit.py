import numpy as np

def slit_fit(image):
    
    peak_pos = np.argmax(image, axis=1)
    
    good_pk_pos = peak_pos[100:2500]
    
    xrange = np.arange(100, 2500, 1)
    
    fit = np.poly1d(np.polyfit(xrange, good_pk_pos, 3))
    
    return fit
    
    