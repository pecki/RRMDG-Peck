# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 18:39:27 2018

@author: pecki
"""

def get_3Dadult(text):
    import math
    import numpy as np
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
    
    mtx = get_den_list(text)
    
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
    
    for key in dims.keys():
        if key in text:
            correct = dims[key]
            
    xdim = math.ceil(float(correct[3]))
    ydim = math.ceil(float(correct[4]))
    zdim = math.ceil(float(correct[5]))
    
    
    ii = 0
    a = []
    while ii + xdim <= len(mtx):
        a.append(np.array(mtx[ii:ii+xdim]))
        ii += xdim
    
    jj = 0
    b = []
    while jj + ydim <= len(a):
        b.append(np.array(a[jj:jj+ydim]))
        jj += ydim
    
    return b

def get_3Dped(path):
    import numpy as np
    import os
    from PIL import Image
    from numpy import array
    directory = os.fsencode(path)
    all_slices = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"):
            img = Image.open(path + "\\" + filename).convert("L")
            arr = array(img)
            blk = 0.001293
            wte = 1.92
            gy = 1.02
            dens = []
            for row in arr:
                line = []
                for pix in row:
                    if pix <= 10:
                        line.append(blk)
                    elif pix >= 245:
                        line.append(wte)
                    else:
                        line.append(gy)
                dens.append(np.array(line))
            all_slices.append(np.array(dens))
            
    return all_slices