import glob

import astropy.io.fits as fits

biaspath = "/home/ryan/projects/CHARMKASTR/raw/data-2017-08-12-shane-Adam.Burgasser/red/test1035/bias/"

flatpath = "/home/ryan/projects/CHARMKASTR/raw/data-2017-08-12-shane-Adam.Burgasser/red/test1035/flat/"

sciencepath = "/home/ryan/projects/CHARMKASTR/raw/data-2017-08-12-shane-Adam.Burgasser/red/test1035/science/"

arcpath = "/home/ryan/projects/CHARMKASTR/raw/data-2017-08-12-shane-Adam.Burgasser/red/test1035/arc/"

BIAS = []

FLAT = []

SCIENCE = []

ARC = []

for filename in glob.glob(biaspath + '*.fits'):
    BIAS.append(fits.open(filename))

for filename in glob.glob(flatpath + '*.fits'):
    FLAT.append(fits.open(filename))

for filename in glob.glob(sciencepath + '*.fits'):
    SCIENCE.append(fits.open(filename))

for filename in glob.glob(arcpath + '*.fits'):
    ARC.append(fits.open(filename))

