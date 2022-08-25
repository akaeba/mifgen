#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:        Andreas Kaeberlein
@copyright:     Copyright 2022
@credits:       AKAE

@license:       GPLv3
@maintainer:    Andreas Kaeberlein
@email:         andreas.kaeberlein@web.de

@file:          mif.py
@date:          2022-08-23

@note:          Converts to Altera MIF format
                  Anaconda: run ./mif.py [args]

@see:           https://gist.github.com/mgerst/62794cbbe672d4039b9e#file-convert_to_mif-py
@see:           https://www.intel.com/content/www/us/en/programmable/quartushelp/17.0/reference/glossary/def_mif.htm
@see:           https://faculty-web.msoe.edu/johnsontimoj/EE3921/files3921/mif_file_format.pdf
"""


import os
import argparse
from datetime import datetime


parser = argparse.ArgumentParser(description='A script to convert binary assembly to a mif file')

parser.add_argument('infile', nargs=1, help='Input File', metavar='FILE')
parser.add_argument('outfile', nargs=1, help='Output Assembly File', metavar='FILE')

parser.add_argument('-d', '--depth', nargs=1, type=int, default=1024)
parser.add_argument('-w', '--width', nargs=1, type=int, default=1, choices=[1, 2, 4, 8])
parser.add_argument('-e', '--endianness', nargs=1, type=str, default='big', choices=['big', 'little'])
args = parser.parse_args()


# open infile for read
vals = [];
if ( '.bin' == (os.path.splitext(args.infile[0])[-1]).lower() ):
    with open(args.infile[0], 'rb') as binfile:
        val=binfile.read(args.width[0])
        while val:
            val=int.from_bytes(val, byteorder=''.join(args.endianness))
            vals.append(val)
            val=binfile.read(args.width[0])
else:
    raise ValueError("Unsupported file type: '" + os.path.splitext(args.infile[0])[-1] + "'")

# write MIF file out
with open(args.outfile[0], 'w') as mif:
    # write header
    mif.write("-- auto generated memory initialization file (mif)\n")
    mif.write("-- source : " + args.infile[0] + "\n")
    mif.write("-- size   : " + str(len(vals)*args.width[0]) + " bytes (" + str(len(vals)) + " words)\n")
    mif.write("-- build  : " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    mif.write("\n")
    # write data header
    mif.write("DEPTH = {}; -- number of words\n".format(args.depth[0]))
    mif.write("WIDTH = {}; -- word width\n".format(8*args.width[0]))
    mif.write("ADDRESS_RADIX = HEX;\n")
    mif.write("DATA_RADIX = HEX;\n\n")
    mif.write("CONTENT\n")
    mif.write("BEGIN\n")
    mif.write("\n")
    # some prepare
    adrPad=len('{:x}'.format(args.depth[0]))    # calc number of digits of address
    # write data
    for i in range(args.depth[0]):
        if ( i < len(vals) ):
            mif.write('{:x}'.format(i).zfill(adrPad) + " : " + '{:x}'.format(vals[i]).zfill(2*args.width[0]) + ";\n")
        else:
            mif.write('{:x}'.format(i).zfill(adrPad) + " : " + "F" * 2*args.width[0] + ";\n") # fill with empty lines
    # done
    mif.write("\n")
    mif.write("END\n")
