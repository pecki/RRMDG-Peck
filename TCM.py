# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 14:27:52 2017

@author: pecki
"""
### In this function there are 9 parameters and they should be as follows:
    # text -> .txt file containing const_z density array
    # stn -> "Y" or "N", representing whether we want multiple z-slices
    # z_1 -> first slice index included if stn == "Y", 0 if "N"
    # z_2 -> first slice index not included (last+1) if "Y", 1 if "N"
    # ct -> "Y" or "N", representing whether we want to choose scan settings
    # start_cm -> user-selected settings, beginning value for scan
    # end_cm -> ending value for scan
    # beam -> value for beam width
    # pitch -> value for pitch of machine
    # wr -> write list of relative intensities to a file?  Yes=True, No=False

def TCM_axial(text, stn, z_1, z_2, ct, start_cm, end_cm, beam, pitch, wr):

    import numpy as np
    import os.path
    import sys
    import os
    sys.path.append(os.path.join(os.getcwd(), 'FileIO'))
    import FileIO as fio
    
    if os.path.isfile(text) == False:
        return 'This file does not exist in the same directory as this program.'
    
    ## to read in density array from text file
    def get_den_list(fi):
        s = open(fi, 'r')
        for line in s:
            de = line.split(' ')
        dens = []
        for x in de:
            if x == '':
                continue
            y = float(x)
            dens.append(y)
        return dens
    
    
    const_z = get_den_list(text)
        
    # Function to find the exponential absorption value
    def exp(mass_atten, rho, t):
        absorption = np.exp(-mass_atten*rho*t)
        return absorption
    
    # Finds the average density for a section of the phantom from z_1 to z_2
    scanrange = True
    if stn == 'y' or stn == 'Y':
        while scanrange == True:
            if z_1 < 0 or z_2 not in range(len(const_z)+1) or z_2 < z_1: # checks for validity of input
                scanrange = True
                return 'Invalid z-slice input(s)'
            else:
                scanrange = False
                sub_dens = const_z[z_1:z_2]
                vol_avg = sum(sub_dens)/len(sub_dens)
                
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
                    
                z_sli_I0 = []
                i = 0
                rho = vol_avg
                mass_atten = 1
                while i < len(sub_dens):
                    I_const = 1
                    t = z_cyl[i]
                    I_0 = I_const/exp(mass_atten, rho, t)
                    z_sli_I0.append(I_0)
                    i += 1
                if wr == True:
                    sp = text.strip('.txt')
                    F = sp + 'int.txt'
                    file = open(F, 'w+')
                    for each in z_sli_I0:
                        num = str(each)
                        file.write(num + ' ')
                    file.close()
                #print("DENS LIST Z:", sub_dens)
                #print("AVERAGE DENSITY:", vol_avg)
    
    
    # Allows user to use a slice thickness that is not the same as the voxel z-dimension
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
            if key in text:
                correct = dims[key]
        width = beam*pitch
        startcm = min(start_cm, end_cm)
        endcm = max(start_cm, end_cm)
        errors = []
    # These if statements ensure that the starting and ending slice values are 
    # valid, and that the beam width is valid with these slice values
        if beam == 0 or startcm == endcm or pitch == 0:
            errors.append('The beam width cannot be 0.')
        else:
            num_slice = (endcm - startcm)/width
        if startcm < 0:
            errors.append('The starting value cannot be negative.')
        if endcm > float(correct[8]):
            errors.append('The ending value cannot be greater than the total z-dimension\
 of the phantom.')
        if beam != 0 and num_slice < 1 and num_slice > 0:
            errors.append('Make sure the beam width is not larger than the start/end range.')
        if len(errors) > 0:
            return "ERROR(S): {}".format(errors)
        
    # Makes a list of edge values of slices - the total number of slices will
    # be one less than the length of the list of edge values
        s = startcm
        bounds = []
        print(width)
        while s <= endcm:
            rem = round((endcm - s), 5)
            if rem > width:
                bounds.append(round(s, 3))
            elif rem <= width and rem != 0:
                bounds.append(round(s, 3))
                bounds.append(round(endcm, 3))
                break
            elif rem == 0:
                bounds.append(round(s, 3))
                break
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
            start_frac = round(float(1 - ((round(bounds[i], 10) % round(z_vox, 10)) / z_vox)), 10)
            end_frac = round(float((bounds[i+1] % z_vox) / z_vox), 10)
            start_z = int(start_z)
            end_z = int(end_z)
            print((round(bounds[i], 2) % round(z_vox, 2)))
           # print(bounds[i+1] % z_vox)
           # print(start_z, end_z)
            print(start_frac, end_frac)
           # print(const_z[start_z:end_z+1])

            slice_sum = 0
            for z in const_z[start_z:end_z+1]:
                #print(slice_sum)
                #print(z)
                #print(const_z.index(z))
                if start_z == end_z:
                    slice_sum += z
                elif const_z.index(z) == start_z:
                    zf = start_frac * z_vox / width
                    #print(zf)
                    slice_sum += (z * zf)
                elif const_z.index(z) == end_z:
                    zf = end_frac * z_vox / width
                    #print(zf)
                    slice_sum += (z * zf)
                else:
                    zf = z_vox / width
                    #print(zf)
                    slice_sum += (z * zf)
            slice_avgs.append(slice_sum)
    
            i += 1
        print("DENS LIST CT:", slice_avgs)
        
    # Finds average density over the whole volume/range of the scan
    # and compares each slice average density to the volume density to find
    # the ratio that is the diameter of each uniform-density cylinder
        CT_avg_vol = sum(slice_avgs) / len(slice_avgs)
        CT_diameters = []
        for d in slice_avgs:
            rat = d / CT_avg_vol
            CT_diameters.append(rat)
    
    
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

        print('AVERAGE DENSITY CT:', CT_avg_vol)
    
    if stn == "Y" and ct == "Y":
        return "\nInitial intensitites I_0 for each slice needed such that\
 the projection intensity I stays constant are shown: {} \nInitial\
 intensities I_0 needed such that the projection intensity I stays constant\
 are shown: {}".format(z_sli_I0, zI0)
    elif stn == "Y" and ct == "N":
        return "\nInitial intensitites I_0 for each slice needed such that\
 the projection intensity I stays constant are shown: {}".format(z_sli_I0)
    elif stn == "N" and ct == "Y":
        return "\nInitial intensities I_0 needed such that the projection intensity\
 I stays constant are shown: {}".format(zI0)

        
print(TCM_axial('rpi_obese_male_117.txt', 'Y', 0, 509, 'N', 0, 0, 0, 0, True))