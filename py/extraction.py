import numpy as np
import copy
import astropy.io.fits as fits

'''
function median() takes a list of astropy HDUL
and returns the median of the data as a 2D
numpy array; used to make median frames
'''
def median(HDUL):

    #list to hold the data
    DLIST = []

    #from the list of hdul, get data from primary hdu and put into list
    for i in range(len(HDUL)):
        DLIST.append(HDUL[i][0].data)

    #construct 3D data cube
    a = np.array(DLIST)
   
    #get the median along the 0th axis; along images
    m = np.median(a, axis=0)

    return m


def bias_subtract(image, bias):
    subtr = image - bias

    return subtr


def create_mask(flat, bias):
    
    subtr = bias_subtract(flat, bias)
    
    mask = copy.deepcopy(subtr)
    s = copy.deepcopy(subtr)
    t = copy.deepcopy(subtr)

    medx = np.median(s, axis=0)
    medy = np.median(t, axis=1)


    for i in range(s.shape[0]):
        for j in range(s.shape[1]):
            if (medx[j] < 5000):
                s[i][j] = 1
            else:
                s[i][j] = 0

    for j in range(t.shape[1]):
        for i in range(t.shape[0]):
            if (medy[i] < 50):
                t[i][j] = 1
            else:
                t[i][j] = 0

    for i in  range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if (s[i][j] == 1 or t[i][j] == 1):
                mask[i][j] = 1

            else:
                mask[i][j] = 0

    return mask


def normalize_flat(flat, mask):

    f = copy.deepcopy(flat)

    m = copy.deepcopy(mask)

    GOOD_PIXELS = []

    for i in range(f.shape[0]):
        for j in range(f.shape[1]):
            if m[i][j] == 0:
                GOOD_PIXELS.append(f[i][j])


    median = np.median(GOOD_PIXELS)
    
    maximum = np.amax(GOOD_PIXELS)

    f = np.divide(f, median)

    return f


def variance_image( image ):
    
    #gains are in units [e-/DN]
    gain_slow = 1.9

    gain_fast = 0.55

    #Shane KAST red read noise are in units [e-]
    read_noise_slow = 3.8

    read_noise_fast = 4.3
    
    var_img = copy.deepcopy(image)

    with np.nditer(var_img, op_flags=['readwrite']) as it:
        for x in it:
            x[...] = ( (np.divide(x,gain_slow)) + np.power(read_noise_slow, 2) ) * (np.power( gain_slow, 2 ))

    return var_img


def normalize_image(image, norm_flat, mask):
    
    norm_image = copy.deepcopy(image)
    
    nf = copy.deepcopy(norm_flat)

    m = copy.deepcopy(mask)

    for i in range(nf.shape[0]):
        for j in range(nf.shape[1]):
            if m[i][j] == 0:
                norm_image[i][j] = np.divide(norm_image[i][j], nf[i][j])

    return norm_image


def mask_image(image, mask):
    
    masked_image = copy.deepcopy(image)
    
    image_median = np.median(masked_image)
    
    for i in range(len(masked_image)):
        for j in range(len(masked_image[i])):
            if mask[i][j] == 1:
                masked_image[i][j] = image_median
                
    return masked_image


def slit_fit(image):
    
    peak_pos = np.argmax(image, axis=1)
    
    good_pk_pos = peak_pos[100:2500]
    
    xrange = np.arange(100, 2500, 1)
    
    fit = np.poly1d(np.polyfit(xrange, good_pk_pos, 3))
    
    return fit


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


def extract_spectrum(image, slit_fit, weight_func):
    
    cent_slc = []
    
    for i in range(len(image[:,0])):
        slc = image[i,:]
        
        cent_slc.append(slc[ int(slit_fit(i) - 10):int(slit_fit(i) + 10)])
    
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


