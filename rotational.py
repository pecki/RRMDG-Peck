# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 22:21:51 2018

@author: pecki
"""

import os
from PIL import Image
import numpy as np
from numpy import array
import time

def mat2d(path):
    directory = os.fsencode(path)
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
    return dens

print(mat2d("C:\\Users\\pecki\\Dropbox\\Research\\all files\\05f"))