#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 18:06:59 2021

@author: feynman
"""


import os
import glob
import numpy as np






def get_name(file_location):
    filename = file_location.split('/')[-1]
    filename = filename.split('.')
    return filename[0]


file_dir = '/home/feynman/Planet/WR_timeline/NIR_G_R_mosaics'


for file in glob.glob(file_dir + '/*.tif'):
    
    fn = get_name(file)
    fn = fn.replace('(', '')
    fn = fn.replace(')', '')
    os.rename(file, file_dir + '/%s.tif'%fn)




