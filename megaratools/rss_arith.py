#
# Copyright 2020-2022 Universidad Complutense de Madrid
#
# This file is part of Megara Tools
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

def main(args=None):
    import astropy.io.fits as fits
    import argparse
    import numpy as np
        
    parser = argparse.ArgumentParser(description='Combining by averaging aligned RSS files',prog='rss_arith')
    parser.add_argument("rss",help="Input table with list of RSS files",type=argparse.FileType('rb'))
    parser.add_argument('-e', '--equation', metavar='Equation to evaluate', help='Example: \'(ima1[:,9] + ima2[:,10])/ ima3[:,3]\'')
    parser.add_argument('-o', '--output', default='combined_rss.fits', metavar='OUTPUT RSS', help='Output RSS', type=argparse.FileType('w'))

    args = parser.parse_args(args=args)

    list_files = args.rss.readlines() 
    list_files = [str(x.strip(),'utf-8') for x in list_files] 

    for x in range(0,len(list_files)):
        globals()['ima%s' % (x+1)] = fits.open(list_files[x])[0].data
    
    refima = fits.open(list_files[0])
    data1 = refima[0].data

    chars = ["[", "]"]
    channel = any([char in args.equation for char in chars])
    if (channel):
       avgdata = np.zeros([data1.shape[0],1])
       avgdata[:,0] = eval(args.equation)
    else:
       avgdata = np.zeros([data1.shape[0],data1.shape[1]])
       avgdata = eval(args.equation)

    refima[0].data = avgdata
    refima.writeto(args.output.name, overwrite = True)

if __name__ == '__main__':

    main()
