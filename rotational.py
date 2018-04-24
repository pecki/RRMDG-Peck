# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 22:21:51 2018

@author: pecki
"""

### PARAMETERS ###
# type_ap -> 'a'=adult or 'p'=pediatric - determines how matrix is retrieved
# getfile -> mtx text file name for adult, directory path for child
# intlist -> file name of average slice intensity .txt file


def TCM_rot(type_ap, getfile, intlist):
    import numpy as np
    from numpy import pi
    import time
    from getmtx import get_3Dadult
    from getmtx import get_3Dped
    s = time.time()
    
    if type_ap == 'a':
        mtx3D = get_3Dadult(getfile)
        vox_t = .35
    elif type_ap == 'p':
        mtx3D = get_3Dped(getfile)
        vox_t = .2
    
    def get_I(mtx0, mtx90, thickness, I_slice):
        beams0 = []
        for row in mtx0:
            p0t0 = 0
            for column in row:
                p0t0 += column
            beams0.append(p0t0)
            
        beams90 = []
        for row in mtx90:
            p90t90 = 0
            for column in row:
                p90t90 += column
            beams90.append(p90t90)
        
        avg0 = sum(beams0)/len(beams0)
        avg90 = sum(beams90)/len(beams90)
        
        e0 = np.exp(-thickness*avg0)
        e90 = np.exp(-thickness*avg90)
        
        I90 = 2*I_slice / (1 + (e90/e0))
        I0 = 2*I_slice - I90
        
        theta = 0
        angles = {}
        while theta < 2*pi:
            y = np.sqrt(I90**2 / (np.tan(theta)**2 + (I90 / I0)**2))
            x = np.tan(theta) * y
            r = round(np.sqrt(x**2 + y**2), 2)
            angles[round((theta * 180/pi), 2)] = r
            theta += pi / 8
    
        return angles
    
    def get_int_list(fi):
        s = open(fi, 'r')
        for line in s:
            de = line.split(' ')
        ints = []
        for x in de:
            if x == '':
                continue
            y = float(x)
            ints.append(y)
        return ints
    
    slice_Is = get_int_list(intlist)
    print(len(slice_Is))
    
    intensities = []
    i = 0
    for z in mtx3D:
        I_sl = slice_Is[i]
        zt = np.transpose(z)
        intensities.append(get_I(z, zt, vox_t, I_sl))
        i += 1
    
    e = time.time()
    print("Time elapsed:", (e-s), "sec")

    print(len(intensities))
    return intensities

print(TCM_rot('a', 'rpi_obese_female_89mtx.txt', 'rpi_obese_female_89int.txt'))