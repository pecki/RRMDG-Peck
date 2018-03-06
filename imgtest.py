# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 20:20:17 2018

@author: pecki
"""
import os
from PIL import Image
from numpy import array
import time


def get_dens_from_image(path):
    sp = path.split('\\')
    nm = sp[len(sp)-1]
    directory = os.fsencode(path)
    const_z = []
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
                dens.append(line)
            new = []
            for row in dens:
                for col in row:
                    new.append(col)
            avgslice = sum(new) / len(new)
        const_z.append(avgslice)
    F = nm + 'dens.txt'
    file = open(F, 'w+')
    for each in const_z:
        num = str(each)
        file.write(num + ' ')
    file.close()
    
    return const_z

s = time.time()
print(get_dens_from_image("C:\\Users\\pecki\\Dropbox\\Research\\05f"))
e = time.time()
print("Time elapsed:", (e-s), "sec")