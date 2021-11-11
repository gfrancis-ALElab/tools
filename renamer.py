#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 18:06:59 2021

@author: feynman
"""


import os
import glob
import numpy as np
from natsort import natsorted




def get_name(file_location):
    filename = file_location.split('/')[-1]
    filename = filename.split('.')
    return filename[0], filename[1]


lib = '/home/feynman/Planet/WR_Timeline/WR_Timeline_Maps/'


for file in natsorted(glob.glob(lib + '/WR*')):
    
    fn, ext = get_name(file)
    fn = fn.replace('WR', '')
    # fn = fn.replace('WR', '')
    # print(fn, ' ', ext)
    os.rename(file, lib + '/%s.%s'%(fn,ext))



# print('Re-numbering...')
# count = 0
# for pic in natsorted(glob.glob(lib + '/*.png')):
#     num = int(get_name(pic))
#     num += 107
#     os.rename(pic, lib + '/%s.png'%num)
#     # count += 1
#     # if count > 10: break
# count = 0
# # for pic in glob.glob(lib + '/*.tif'):
#     # os.rename(pic, lib + '/%s.tif'%count)
#     # count += 1



