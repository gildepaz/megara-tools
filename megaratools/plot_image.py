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
plt.rcParams.update({'mathtext.default':  'regular' })
import astropy.io.fits as fits
import argparse
from astropy.wcs import WCS
import sys
import csv

def main(args=None):
# Parser
    parser = argparse.ArgumentParser(description='Visualize image',prog='plot_image')
    parser.add_argument('-i', '--image', metavar='Image', help='FITS image', type=argparse.FileType('rb'))
    parser.add_argument('-c', '--channel', metavar='Channel', help='Channel to image', type=int)
    parser.add_argument('-z1', '--zmin', metavar='Lower cut', help='Lower cut to plot', type=float)
    parser.add_argument('-z2', '--zmax', metavar='Upper cut', help='Upper cut to plot', type=float)
    parser.add_argument('-m', '--map', metavar='Color map', help='String of color map (cmap)')
    parser.add_argument('-t', '--title', metavar='Plot title', help='Title of the plot')
    parser.add_argument('-C', '--draw-contours', default=False, action="store_true", help='Draw contours?')
    parser.add_argument('-I', '--image-contours', metavar='IMAGE4CONTOURS', help='Image for contours', nargs='*')
    parser.add_argument('-cc', '--cchannel', metavar='RSS CHANNEL CONTOURS', help='Channel of RSS product for contours', type=int)
    parser.add_argument('-CZ1', '--czcut1', metavar='LOWER CUT LIMIT CONTOURS', default=0., help='Lower cut limit for plot', type=float)
    parser.add_argument('-CZ2', '--czcut2', metavar='UPPER CUT LIMIT CONTOURS', default=0.0005, help='Upper cut limit for plot', type=float)
    parser.add_argument('-S', '--s-contours', metavar='STEP CONTOURS', default=0.000025, help='Step between contours', type=float)
    parser.add_argument('-pc', '--palette-contours', metavar='PALETTE', help='Palette for contours')

    args = parser.parse_args(args=args)

    image = args.image
    img = fits.open(image)
    data = img[0].data[args.channel,:,:]
    hdr = img[0].header
    fig = plt.figure(figsize=(hdr['NAXIS1']/30,hdr['NAXIS2']/30))
    wcs2 = WCS(hdr).celestial
    ax = fig.add_axes([0.15, 0.1, 0.8, 0.8], projection=wcs2, label='Dec')
    ax.tick_params(axis='both', labelsize=12)

    if args.draw_contours:
        for ima in args.image_contours:
            fnamec = ima
            imgc = fits.open(fnamec)
            datac = imgc[0].data[args.cchannel,:,:]

    if (args.zmin is None and args.zmax is None): 
       plt.imshow(data, cmap=args.map)
    else:
       plt.imshow(data, cmap=args.map, vmin=args.zmin, vmax=args.zmax)

    if args.draw_contours:
       levels = np.arange(args.czcut1, args.czcut2, args.s_contours)
       czorder=30
       col = plt.contour(datac, levels, colors=args.palette_contours, zorder=czorder)

    ax.set_xlabel('RA (J2000)')
    ax.set_ylabel('Dec (J2000)')
    ax.set_title(args.title)
    plt.colorbar()
    plt.show()

if __name__ == '__main__':

    main()

