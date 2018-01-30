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

# Finds and specifies the dimensions of the phantom using the "fill=" line
# at the beginning of the geometry file

def get_dims(f):
    c = []
    phant_dims = []
    for line in open(f, 'r'):
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
    return phant_dims

phant_dims = get_dims(geo)


# Uses an imported function to create an array containing (phant_dims[0]*
# phant_dims[1]*phant_dims[2]) entries which are number IDs representing 
# materials for which data is also included in the phantom geometry file
phantom1D = fio.ImportPhantom(geo, phant_dims, verbose = True)


# Creates a list (materials) of sublists, with each sublist containing
# bits of information about each organ/material, corresponding to the ID numbers
def densities(f):
    materials = []
    air = 0
    for line in open(f, 'r'):
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
    densities = np.array(density_list)
    return densities

dens_array = densities(geo)
# Prints all the useful information
print('The dimensions of the phantom in [x,y,z] form are:', phant_dims)
print('This indicates that there are', phant_dims[0]*phant_dims[1]*phant_dims[2], 'voxels in total.')
print('\nThe phantom array containing all the ID numbers for each voxel:')
print('phantom1D =', phantom1D)
print('\nThe phantom array containing all the density values corresponding\
 to the ID numbers in the original array:')
print('densities =', dens_array)
print('\nThe length of the phantom1D array is ' , len(phantom1D), '\
 and the length of the densities array is ', len(dens_array), '.  Both should\
 match the total number of voxels analyzed.', sep='')

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
    
print(const_z)