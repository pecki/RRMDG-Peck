# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 16:59:25 2018

@author: pecki
"""
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

print(len(get_den_list("rpi_obese_female_122int.txt")))