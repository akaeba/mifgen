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
                  Anaconda: run ./mif.py --size=<size> --width=<width> <infile>

@see:           https://github.com/akaeba/mif
"""


import os
import argparse
from datetime import datetime


# CLI Parser
parser = argparse.ArgumentParser(description='A script to convert binary assembly to a mif file')

parser.add_argument('infile', nargs=1, help='Input File', metavar='FILE')

parser.add_argument('-o', '--outfile', nargs=1, type=str, default='', help='Output MIF File')
parser.add_argument('-s', '--size', nargs=1, type=str, default='1024', help='MIF outfile size in byte')
parser.add_argument('-w', '--width', nargs=1, type=int, default=1, choices=[1, 2, 4, 8], help='Number of bytes per word')
parser.add_argument('-e', '--endianness', nargs=1, type=str, default='big', choices=['big', 'little'], help='Endianness of output file')
args = parser.parse_args()


# convert size
args.size=''.join(args.size)    # make single string
siexp='KMG'.find(args.size[-1]) # get position of si prefix
if ( -1 != siexp ):
    args.size = float(args.size[:-1]) * pow(1024, siexp+1)
    args.size = int(round(args.size, 0))
else:
    try:
        args.size = int(args.size)
    except:
        raise ValueError('Unsupported --size argument "' + args.size + '"')

# check for mulitple in words
if ( 0 != (args.size % args.width[0])):
    raise ValueError('--size=' + str(args.size) + ' is not an multiple of --width=' + str(args.width[0]))
depth = int(round(args.size / args.width[0]))

# default outfile
if ( 0 == len(''.join(args.outfile))):
    args.outfile = os.path.splitext(args.infile[0])[0] + '.mif'

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

# check for truncation
if ( args.size < (len(vals)*args.width[0]) ):
    raise ValueError('BIN File (size=' + str(len(vals)*args.width[0]) + ') is larger then targeted MIF file (size=' + str(args.size) + ')')

# write MIF file out
with open(''.join(args.outfile), 'w') as mif:
    # write header
    mif.write("-- auto generated memory initialization file (mif)\n")
    mif.write("-- https://github.com/akaeba/mif\n")
    mif.write("--\n")
    mif.write("-- source   : " + args.infile[0] + "\n")
    mif.write("-- build    : " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    mif.write("-- bin size : " + str(len(vals)*args.width[0]) + " bytes (" + str(len(vals)) + " words)\n")
    mif.write("-- mif size : " + str(args.size) + " bytes (" + str(depth) + " words)\n")
    mif.write("\n")
    mif.write("\n")
    # write data header
    mif.write("DEPTH = {}; -- number of words\n".format(depth))
    mif.write("WIDTH = {}; -- word width\n".format(8*args.width[0]))
    mif.write("ADDRESS_RADIX = HEX;\n")
    mif.write("DATA_RADIX = HEX;\n\n")
    mif.write("CONTENT\n")
    mif.write("BEGIN\n")
    mif.write("\n")
    # some prepare
    adrPad=len('{:x}'.format(depth))    # calc number of digits of address
    # write data
    for i in range(depth):
        if ( i < len(vals) ):
            mif.write('{:x}'.format(i).zfill(adrPad) + " : " + '{:x}'.format(vals[i]).zfill(2*args.width[0]) + ";\n")
        else:
            mif.write('{:x}'.format(i).zfill(adrPad) + " : " + "F" * 2*args.width[0] + ";\n") # fill with empty lines
    # done
    mif.write("\n")
    mif.write("END\n")
