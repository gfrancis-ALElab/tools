# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 11:43:23 2021

@author: gfrancis
"""



import os
### Set OSGEO env PATHS
home = os.path.expanduser('~')
os.environ['PROJ_LIB'] = '/usr/share/proj'
os.environ['GDAL_DATA'] = '/usr/share/gdal'
import glob
import osgeo_utils


gdal_merge = home + '/repos/tools/gdal_merge.py'
top_folder = home + '/Planet/HWC_Timeline/downloads/**/files'
out_dir = home + '/Planet/HWC_Timeline/mosaics'



for directory in glob.glob(top_folder):
    
    name = directory[51:59]
    # print(name)
    out_file = out_dir + '/' + name + '.tif'
    os.system('echo merging: %s'%name)
    
    pieces = ''
    for piece in glob.glob(directory + '/*SR_clip.tif'):
        pieces += ' ' + piece
    
    os.system('sudo python ' + gdal_merge + ' -o ' + out_file + pieces)
    
    






