# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 22:21:51 2018

@author: pecki
"""

import numpy as np
import os
from PIL import Image
from numpy import array
import time

s = time.time()

path = "C:\\Users\\pecki\\Dropbox\\Research\\all files\\10f"
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
        
print(len(all_slices))

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

    return (I0, I90)

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
            
slice_Is = get_den_list("10fdens.txt")
intensities = []
i = 0
for z in all_slices:
    t = .2
    I_sl = slice_Is[i]
    zt = np.transpose(z)
    intensities.append(get_I(z, zt, t, I_sl))
    i += 1

print(len(intensities))
print(intensities)

e = time.time()
print("Time elapsed:", (e-s), "sec")