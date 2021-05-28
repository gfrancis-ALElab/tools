# -*- coding: utf-8 -*-
"""
Created on Mon May 10 15:52:58 2021


Tool for creating a 3band (NIR,G,R) image from 4band Planet Scope images


@author: Grant Francis
email: gfrancis@uvic.ca
"""

import os
home = os.path.expanduser('~')
### Set OSGEO env PATHS
os.environ['PROJ_LIB'] = home + r'\Appdata\Roaming\Python\Python37\site-packages\osgeo\data\proj'
os.environ['GDAL_DATA'] = home + r'\Appdata\Roaming\Python\Python37\site-packages\osgeo\data'
import rasterio
import numpy as np
import glob
import geopandas as gpd
from shapely import speedups
speedups.disable()








lib = r'C:\Users\gfrancis\Documents\Planet\SuperReg\originals'
out = r'C:\Users\gfrancis\Documents\Planet\SuperReg\NIR_G_R_standardized'
### Get CRS from truths used
truths_path = r'C:\Users\gfrancis\Documents\Planet\WR\Data\ground_truths\Willow_River_Thaw_Slumps_poly.shp'

truths = gpd.read_file(truths_path)
crs = truths.crs




def get_name(file_location):
    filename = file_location.split('\\')[-1]
    filename = filename.split('.')
    return filename[0]



for pic in glob.glob(lib + '\\*.tif'):

    ras = rasterio.open(pic)
    name = get_name(pic)
    
    if ras.meta['count'] == 4:
        bandRed = ras.read(3)
        bandgreen = ras.read(2)
        bandNIR = ras.read(4) ### NIR is channel 4 in Planet Scope 4band 
        
    if ras.meta['count'] == 5:
        bandRed = ras.read(3)
        bandgreen = ras.read(2)
        bandNIR = ras.read(5) ### NIR is channel 5 in Rapid Eye 5band
    
    NIR_arr = bandNIR.astype(float)
    green_arr = bandgreen.astype(float)
    red_arr = bandRed.astype(float)
    
    
    if NIR_arr.min() == 0:
        NIR_arr = np.where(NIR_arr==0, 65535, NIR_arr)
        green_arr = np.where(green_arr==0, 65535, green_arr)
        red_arr = np.where(red_arr==0, 65535, red_arr)
    
    
    NIR_arr = (NIR_arr/NIR_arr.max())*255
    green_arr = (green_arr/green_arr.max())*255
    red_arr = (red_arr/red_arr.max())*255
    
    
    NIR_arr = NIR_arr.astype(np.uint8)
    green_arr = green_arr.astype(np.uint8)
    red_arr = red_arr.astype(np.uint8)
    
    
    
    kwargs3band = ras.meta
    kwargs3band.update(
        dtype=rasterio.uint8,
        nodata=255,
        crs=crs,
        count=3)
    
    print(kwargs3band)
    print('\n')
    
    with rasterio.open(out + '\\%s_NIR_G_R.tif'%name, 'w', **kwargs3band) as dst5:
        dst5.write_band(1, NIR_arr.astype(rasterio.uint8))
        dst5.write_band(2, green_arr.astype(rasterio.uint8))
        dst5.write_band(3, red_arr.astype(rasterio.uint8))
        
    
    ras.close()

























