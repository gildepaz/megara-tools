#
# Copyright 2022 Universidad Complutense de Madrid
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
        
    parser = argparse.ArgumentParser(description='Arithmetic on cube files',prog='cube_arith')
    parser.add_argument("cube",help="Input table with list of cubes",type=argparse.FileType('rb'))
    parser.add_argument('-e', '--equation', metavar='Equation to evaluate', help='Example: \'(ima1[:,9] + ima2[:,10])/ ima3[:,3]\'')
    parser.add_argument('-o', '--output', default='result.fits', metavar='OUTPUT CUBE', help='Output cube', type=argparse.FileType('w'))

    args = parser.parse_args(args=args)

    list_files = args.cube.readlines() 
    list_files = [str(x.strip(),'utf-8') for x in list_files] 

    for x in range(0,len(list_files)):
        globals()['ima%s' % (x+1)] = fits.open(list_files[x])[0].data
    
    refima = fits.open(list_files[0])
    data1 = refima[0].data
    avgdata = np.zeros([1,data1.shape[1],data1.shape[2]])
    avgdata[0,:,:] = eval(args.equation)
    
    refima[0].data = avgdata
    refima.writeto(args.output.name, overwrite = True)

if __name__ == '__main__':

    main()
