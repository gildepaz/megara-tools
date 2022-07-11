#
# Copyright 2019-2022 Universidad Complutense de Madrid
#
# This file is part of Megara Tools
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['contour.negative_linestyle'] = 'solid'
import astropy.io.fits as fits
import argparse
from astropy.wcs import WCS
import sys
import csv

def main(args=None):
# Parser
    parser = argparse.ArgumentParser(description='Visualize image',prog='extract_region_cube')
    parser.add_argument('-i', '--image', metavar='Image', help='FITS cube', type=argparse.FileType('rb'))
    parser.add_argument('-x', '--xpos', metavar='X position', default=0.0, help='Position of center in x (pixels)', type=float)
    parser.add_argument('-y', '--ypos', metavar='Y position', default=0.0, help='Position of center in y (pixels)', type=float)
    parser.add_argument('-r', '--radius', metavar='Radius', default=2.0, help='Radius of aperture (pixels)', type=float)
    parser.add_argument('-o', '--output', metavar='OUTPUT-SPECTRUM', help='Output 1D spectrum', type=argparse.FileType('wb'))

    args = parser.parse_args(args=args)

    image = args.image
    ofile = args.output # Output 1D spectrum

    img = fits.open(image)
    tbdata = img[0].data
    prihdr = img[0].header
    naxis1 = prihdr['NAXIS1']
    naxis2 = prihdr['NAXIS2']

    sellist = []
    for ix in range(0,naxis2):
        for iy in range(0,naxis1):
            if (np.sqrt((ix-args.xpos)**2+(iy-args.ypos)**2) < args.radius):
                sellist.append([ix,iy])

    region = tbdata[sellist,:]
    newima = np.sum(region, axis=tuple(range(region.ndim - 1)))

    prihdr['CRVAL1'] = prihdr['CRVAL3']
    prihdr['CRPIX1'] = prihdr['CRPIX3']
    prihdr['CDELT1'] = prihdr['CDELT3']
    prihdr['CTYPE1'] = prihdr['CTYPE3']
    prihdr['CUNIT1'] = prihdr['CUNIT3']
    
    ext_spectrum = fits.PrimaryHDU(newima, header=img[0].header)
    ext_spectrum.header.remove('CRVAL2', ignore_missing=True, remove_all=True)
    ext_spectrum.header.remove('CRPIX2', ignore_missing=True, remove_all=True)
    ext_spectrum.header.remove('CDELT2', ignore_missing=True, remove_all=True)
    ext_spectrum.header.remove('CTYPE2', ignore_missing=True, remove_all=True)
    ext_spectrum.header.remove('CUNIT2', ignore_missing=True, remove_all=True)
    ext_spectrum.writeto(ofile, overwrite=True)

if __name__ == '__main__':

    main()

