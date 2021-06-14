# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 14:10:17 2021

@author: gfrancis
"""


import os
import glob
from PIL import Image
import numpy as np




lib = r'C:\Users\gfrancis\Documents\Planet\WR_timeline\Priority_Regions\differences'


i = 0
for pic in glob.glob(lib + '\\*.jpg'):
    G = Image.open(pic)
    arr_G = np.array(G)
    Image.fromarray(arr_G.astype(np.uint8)).convert('RGB').save(lib + '\\frames\\%04d.jpg'%i)
    i += 1



os.chdir(lib + '\\frames')
os.system('ffmpeg -r 16 -f image2 -i %4d.jpg -s 4608x3456 -c:v mjpeg -q:v 10 ./timelapse.mov')



















