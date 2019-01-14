import numpy as np
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

        
