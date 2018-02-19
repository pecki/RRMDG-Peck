# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 19:55:25 2018

@author: pecki
"""

import numpy as np
import os.path
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'FileIO'))
import FileIO as fio

# Asks the user for the file name for the geometry of the phantom
geo = input('Geometry file name: ')

while os.path.isfile(geo) == False:
    print('This file does not exist in the same directory as this program.')
    geo = input('Geometry file name: ')

########################################################
# Want to take in file name - make function that gets phantom dimensions,
# density array, and average slice density for each slice in the phantom

########################################################
# Finds and specifies the dimensions of the phantom using the "fill=" line
# at the beginning of the geometry file

def write(geo):
    c = []
    phant_dims = []
    for line in open(geo, 'r'):
        if 'fill=0' in line:
            line = line.strip().strip('fill=')
            a = line.split(':')
            for x in a:
                if '0' in x or '&' in x:
                    x = x.strip('0').strip('&').strip()
                c.append(x)
            for y in c:
                if y.isdigit():
                    phant_dims.append(int(y)+1)
                    
    phantom1D = fio.ImportPhantom(geo, phant_dims, verbose = True)
# ^^^ Uses an imported function to create an array containing (phant_dims[0]*
# phant_dims[1]*phant_dims[2]) entries which are number IDs representing 
# materials for which data is also included in the phantom geometry file


# Creates a list (materials) of sublists, with each sublist containing
# bits of information about each organ/material, corresponding to the ID numbers
    materials = []
    air = 0
    for line in open(geo, 'r'):
        if 'vol' in line:
            l = line.split(' ')
            l[:] = [item for item in l if item != '']
            materials.append(l)
    for m in materials:
        if 'airinside' in m:
            air = (float(m[2])*-1)
    
    # Creates a dictionary in which the ID numbers of each material are the keys
    # and the values are the corresponding density values.  Initializes the density
    # of air for later calculations.
    assgn = {}
    for organ in materials:
        o0int = int(organ[0])
        o2flt = float(organ[2])
        assgn[o0int] = o2flt
    
    # Creates an array of the same length and in the same order as the phantom1D
    # array, but with densities for each voxel instead of ID numbers
    density_list = []
    for b in phantom1D:
        val = (assgn[b]*-1)
        density_list.append(val)  
    dens_array = np.array(density_list)

# Creates a list and a dictionary of the average density per constant z (slice)
    const_z = []
    start = 0
    end = phant_dims[0]*phant_dims[1]
    z = 0
    while z <= phant_dims[2]-1:
        D = dens_array[start:end]
        avg = sum(D)/len(D)
        const_z.append(avg)
        z += 1
        start += phant_dims[0]*phant_dims[1]
        end += phant_dims[0]*phant_dims[1]

## F is a file name to be written to
## want to convert each value in const_z to WED, create an array that is written to a file
##  ---> density of water = 1 g/cm^3
    F = geo.strip('.geo') + '.txt'
    file = open(F, 'w+')
    for each in const_z:
        num = str(each)
        file.write(num + ' ')
    file.close()
    
    return const_z


g = write(geo)
print(g)

