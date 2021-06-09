# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 11:43:23 2021

@author: gfrancis
"""



import os
### Set OSGEO env PATHS
home = os.path.expanduser('~')
os.environ['PROJ_LIB'] = home + r'\Appdata\Roaming\Python\Python37\site-packages\osgeo\data\proj'
os.environ['GDAL_DATA'] = home + r'\Appdata\Roaming\Python\Python37\site-packages\osgeo\data'
import glob


gdal_merge = r'C:\Users\gfrancis\Documents\Code\tools\gdal_merge.py'
top_folder = 'C:/Users/gfrancis/Documents/Planet/WR_timline/**/files'
out_dir = r'C:\Users\gfrancis\Documents\Planet\WR_timline\mosaics'



for directory in glob.glob(top_folder):
    
    name = directory[46:62]
    out_file = out_dir + '\\' + name + '.tif'
    os.system('echo merging: %s'%name)
    
    pieces = ''
    for piece in glob.glob(directory + '/*SR_clip.tif'):
        pieces += ' ' + piece
    
    os.system(gdal_merge + ' -o ' + out_file + pieces)
    
    






