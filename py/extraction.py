import numpy as np
import copy
import astropy.io.fits as fits

'''
function cube_median() takes a list of astropy HDUL
and returns the median of the data as a 2D
numpy array; used to make median frames
'''
def cube_median(HDUL):

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


def flat_normalize_image(image, norm_flat, mask):
    
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


def slit_fit_model(image):
    
    peak_pos = np.argmax(image, axis=1)
    
    good_pk_pos = peak_pos[100:2500]
    
    xrange = range(100, 2500)
    
    fit = np.polyfit(xrange, good_pk_pos, 4)
    
    return fit

def slit_fit_trace(model):
    
    fit = np.poly1d(model)
    
    return fit

#TODO create a function to generage centered slices, use them for rest of reduction
#rather than loading in the whole image
#also with a parameter for changing how far from the peak to go

def gen_cent_slc(image, slit_fit, px_from_peak):
    
    cent_slc = []
    
    for i in range(len(image[:,0])):
        slc = image[i,:]
        
        cent_slc.append(slc[ int(np.around(slit_fit(i) - px_from_peak)):int(np.around(slit_fit(i) + px_from_peak))])
        
    return cent_slc

def create_norm_spatial_profile(cent_slcs):
    prof_slcs = copy.deepcopy(cent_slcs)
    for i in range(len(prof_slcs)):
        prof_slcs[i] = prof_slcs[i] / np.amax(prof_slcs[i])
     
    prof = np.median(prof_slcs, axis=0)
    return prof

def background_subtract(c_slc, sp_prof, percent_threshold):
        
    cent_slc = copy.deepcopy(c_slc)
    
    #empty lists to hold the background slices and their indices
    background_slices = []
    '''
       deciding which pixels are background
       background pixels are areas where the spatial
       profile is less than the given threshold
    '''
    for i in range(len(cent_slc)):
        
        #setting up empty lists to hold the background pixels
        background_px = []
        
        
        #if the pixel value in the slice is less than the threshold, it's background
        for j in range(len(cent_slc[i])):
            if (sp_prof[j] < percent_threshold):
                background_px.append(cent_slc[i][j])
        #appending the pixels and indices from this slice to the list for all slices
        
        #if the list isn't empty, append it, otherwise append the orignal slice
        #since it is probably all background in that case
        if background_px != []:
            background_slices.append(background_px)
        else:
            background_slices.append(cent_slc[i])
    
    #empty list to hold the background value
    background_vals = []
    
    #for each slice, find the median and store it
    for i in range(len(background_slices)):
        background_vals.append(np.median(background_slices[i]))
        
    #the signal is the difference between the centered slices and the background
    signal_slc = copy.deepcopy(cent_slc)
        
    for i in range(len(signal_slc)):
        signal_slc[i] = signal_slc[i] - background_vals[i]
    
    return signal_slc, background_vals

def weight_function(c_slc):
    
    cent_slc = copy.deepcopy(c_slc)
    w_slc = []
    
    for i in range(len(cent_slc)):
        slc = cent_slc[i]
        
        smax = np.amax(slc)
        
        if (smax == 0):
            w_slc.append(slc)
            continue
        
        smedian = np.median(slc)
        
        slc = slc - smedian
        
        slc = np.divide(slc, smax)
        
        w_slc.append(slc)
        
    w_func = np.median(w_slc, axis=0)
    
    return w_func


#only works for 4th order, will tweak later
def slit_fit_shift(cent_slices, slit_fit_model, spat_prof, px_thresh):
    signal_center = np.argmax(spat_prof)
    
    offset = signal_center - px_thresh
    
    shifted_model = copy.deepcopy(slit_fit_model)
    
    shifted_model[4] = shifted_model[4] + offset
    
    return shifted_model

def extract_spectrum(cent_slc, weight_func):

    
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


def extract_variance(cent_slc, weight_func):
        
    
    var_slc = copy.deepcopy(cent_slc)
    
    w_func = copy.deepcopy(weight_func)
    
    variance = []
    
    for i in range(len(var_slc)):
        for j in range(len(var_slc[i])):
            var_slc[i][j] = var_slc[i][j] * w_func[j]
            
        variance.append(np.divide(np.sum(var_slc[i]), np.sum(w_func)))
        
    return variance


