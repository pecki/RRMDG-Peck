# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 14:27:52 2017

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

## to read in density array from text file, where ph_fl is str name w/o .geo
def get_den_list(fi):
    ph_fl = fi.strip('.geo')
    txt_f = ph_fl + '.txt'
    s = open(txt_f, 'r')
    for line in s:
        de = line.split(' ')
    dens = []
    for x in de:
        if x == '':
            continue
        y = float(x)
        dens.append(y)
    return dens

const_z = get_den_list(geo)

# Finds the average density for a section of the phantom from z_1 to z_2
stn = input('Do you want to know the average density for multiple z-slices? Y/N: ')
scanrange = True
if stn == 'y' or stn == 'Y':
    while scanrange == True:
        z_1 = int(input('Enter the number (z-value) of the starting (included) slice: '))
        z_2 = int(input('Enter the number (z-value) of the ending (not included) slice: '))
        if z_1 < 0 or z_2 not in range(len(const_z)+1) or z_2 < z_1: # checks for validity of input
            scanrange = True
            print('Invalid slice input(s)')
        else:
            scanrange = False
            sub_dens = const_z[z_1:z_2]
            vol_avg = sum(sub_dens)/len(sub_dens)
            print('The average density for this volume of the phantom is', vol_avg)
            
            # Finds diameter of cylinders with uniform density by taking the ratio of the 
            # density of each slice to the average volume density. Creates both a 
            # dictionary and a list
            z_cyl = []
            z_sli_cyl = {}
            for s in sub_dens:
                num = sub_dens.index(s) + z_1
                ratio = float(round(s/vol_avg, 3))
                z_cyl.append(ratio)
                z_sli_cyl[num] = ratio
    
            print('The diameters of the cylinders for each z slice are shown:', z_sli_cyl)


# Allows user to use a slice thickness that is not the same as the voxel z-dimension
ct = input('Do you want to find the average density for a slice with a \
thickness of your choosing? Y/N: ')
if ct == 'y' or ct == 'Y':
    dims = {}
    # Gets data about phantoms from a text document I created and arranged
    # Puts data in a dictionary for easy access
    for line in open('phantom_dimensions.txt', 'r'):
        if '&' not in line:
            l = line.strip().split('   ')
            phant = l[0]
            l.pop(0)
            if phant in dims.keys():
                for x in l:
                    dims[phant].append(x)
            else:
                dims[phant] = l

# Finds information from dictionary for the current phantom being analyzed
    for key in dims.keys():
        if key in geo:
            correct = dims[key]
    beam = 0
    pitch = 0
    startcm = -1
    endcm = float(correct[8]) + 1
# These if statements ensure that the starting and ending slice values are 
# valid, and that the beam width is valid with these slice values
    while ( beam == 0 or startcm < 0 \
           or endcm > float(correct[8]) or endcm < startcm):
        startcm = float(input('What is the starting value for the section (in cm)? '))
        endcm = float(input('What is the ending value for the section (in cm)? '))
        beam = float(input('What is the width of the x-ray beam (in cm)? '))
        pitch = float(input('What is the pitch of the machine? '))
        width = beam*pitch
        if beam == 0 or startcm == endcm or pitch == 0:
            print('The beam width cannot be 0.')
            continue
        else:
            num_slice = (endcm - startcm)/width
        if startcm < 0:
            print('The starting value cannot be negative.')
        if endcm > float(correct[8]):
            print('The ending value cannot be greater than the total z-dimension \
of the phantom.')
        if endcm < startcm:
            print('Make sure the starting value is less than the ending value.')
        if num_slice < 1 and num_slice > 0:
            print('Make sure the beam width is not larger than the start/end range.')
    
# Makes a list of edge values of slices - the total number of slices will
# be one less than the length of the list of edge values
    s = startcm
    bounds = []
    while s < endcm:
        rem = endcm - s
        if rem < width and rem != 0:
            bounds.append(round(s, 3))
            bounds.append(round(endcm, 3))
            break
        bounds.append(round(s, 3))
        s += width
    print(bounds)

# For each pair of adjacent values in 'bounds', the average density for
# this slice is computed and appended to a list of slice densities
    z_vox = float(correct[2])
    i = 0
    slice_avgs = []
    while i+1 < len(bounds):
        start_z = float(bounds[i]/z_vox)
        end_z = float(bounds[i+1]/z_vox)
        start_frac = round(float(1 - ((bounds[i] % z_vox) / z_vox)), 10)
        end_frac = round(float((bounds[i+1] % z_vox) / z_vox), 10)
        start_z = int(start_z)
        end_z = int(end_z)
        slice_sum = 0
        for z in const_z[start_z:end_z+1]:
            if const_z.index(z) == start_z:
                slice_sum += (z * start_frac)
            elif const_z.index(z) == end_z:
                slice_sum += (z * end_frac)
            else:
                slice_sum += z
        avg_slice = round(slice_sum / (bounds[i+1]-bounds[i]), 10)
        slice_avgs.append(avg_slice)

        i += 1
    
# Finds average density over the whole volume/range of the scan
# and compares each slice average density to the volume density to find
# the ratio that is the diameter of each uniform-density cylinder
    CT_avg_vol = sum(slice_avgs) / len(slice_avgs)
    CT_diameters = []
    for d in slice_avgs:
        rat = d / CT_avg_vol
        CT_diameters.append(rat)


# Function to find the exponential absorption value

def exp(mass_atten, rho, t):
    absorption = np.exp(-mass_atten*rho*t)
    return absorption
    
if ct == 'y' or ct == 'Y':
    zI0 = []
    i = 0
    rho = CT_avg_vol
    mass_atten = 1
    while i < len(slice_avgs):
        I_const = 1
        t = CT_diameters[i]
        I_0 = I_const/exp(mass_atten, rho, t)
        zI0.append(I_0)
        i += 1
    print('\nThe diameters of each slice are shown:', CT_diameters)
    print('\nThe average density over the entire range is:', CT_avg_vol)
    print('\nThe initial intensities I_0 needed such that the projection intensity \
I stays constant are shown:', zI0)