from extraction_scripts import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def standard_reducer(imagepath, outputpath, objectname, bias, norm_flat, mask):
    
    imagefile = fits.open(imagepath)
    print("Loaded image from " + imagepath)
    px_thresh  = int(input("Enter Pixel Radius from Peak: "))
    
    print("Start first stage")
    
    slcs, varslcs, polymod, spat_prof = reduce_standard_first_stage(imagefile, bias, norm_flat, mask, px_thresh)
    
    print("Finish first stage")
    
    modexp = pd.DataFrame(polymod)
    
    modexp.to_csv(outputpath + 'slit_trace_model_' + objectname + '.txt', index=False, header=False)
    
    print("Exported slit trace model to " + outputpath + objectname + '_slit_trace_model.txt')
    
    plt.plot(spat_prof)
    plt.show()
    
    print("Please analyze the spatial profile to select background")                  
    percent_thresh = float(input("Enter Background Threshold: "))
    
    print("Begin second stage")
    spect, variance, bkg = reduce_second_stage(slcs, varslcs, spat_prof, percent_thresh)
                           
    print("Finish second stage")
    
    plt.plot(spect)
    plt.show()
    
    plt.plot(variance)
    plt.show()
                           
    plt.plot(bkg)
    plt.show()
                           
    wavemod = np.loadtxt('/home/ryan/projects/CHARM-KASTr/models/master_wavecal.txt')

    wavecal = np.poly1d(wavemod)
    print("Loaded wavelength calibration model")
    
    pxrange = range(len(spect))
    
    plt.figure(figsize=[12,5])
    plt.plot(wavecal(pxrange), spect)
    plt.xlabel('Wavelength (Angstrom)')
    plt.ylabel('Flux (DN)')
    plt.title(objectname)

    plt.savefig(outputpath + objectname + '.pdf', type='pdf')

    plt.show()
    print("Exported reduced image to " + outputpath + objectname + '.pdf')                        
                           
                           
    PX = pxrange

    WAVELENGTH = wavecal(pxrange)

    FLUX = spect

    STDEV = np.sqrt(variance)

    BKG = bkg

    tuples = list(zip(PX, WAVELENGTH, FLUX, STDEV, BKG))

    head = ['PX', 'WAVELENGTH', 'FLUX', 'STDEV', 'BKG']


    tdf = pd.DataFrame(data=tuples, columns=head)

    tdf.to_csv(outputpath + objectname + ".csv", index=False)
    print("Exported reduced data to " + outputpath + objectname + '.csv')
    print("All done!")