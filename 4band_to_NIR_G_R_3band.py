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








lib = r'C:\Users\gfrancis\Documents\Planet\WR\data\mosaics'
out = r'C:\Users\gfrancis\Documents\Planet\WR\data\NIR_G_R_mosaics'
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
    
    
    ### replace nodata zeros & 65535 to Nan
    if NIR_arr.min() == 0:
        NIR_arr = np.where(NIR_arr==0, np.nan, NIR_arr)
        green_arr = np.where(green_arr==0, np.nan, green_arr)
        red_arr = np.where(red_arr==0, np.nan, red_arr)
    if NIR_arr.max() == 65535:
        NIR_arr = np.where(NIR_arr==65535, np.nan, NIR_arr)
        green_arr = np.where(green_arr==65535, np.nan, green_arr)
        red_arr = np.where(red_arr==65535, np.nan, red_arr)

    
    ### normalize 0 to 1
    NIR_norm = NIR_arr/np.nanmax(NIR_arr)
    green_norm = green_arr/np.nanmax(green_arr)
    red_norm = red_arr/np.nanmax(red_arr)
    
    
    ### center average on 50%
    NIR_norm = NIR_norm + (0.5 - np.nanmean(NIR_norm))
    green_norm = green_norm + (0.5 - np.nanmean(green_norm))
    red_norm = red_norm + (0.5 - np.nanmean(red_norm))
    
    
    # ### scale (0 to 255)
    NIR_scaled = NIR_norm*255
    green_scaled = green_norm*255
    red_scaled = red_norm*255
    
    
    ### change dtype
    NIR_scaled = NIR_scaled.astype(np.uint8)
    green_scaled = green_scaled.astype(np.uint8)
    red_scaled = red_scaled.astype(np.uint8)
    
    
    kwargs3band = ras.meta
    kwargs3band.update(
        dtype=rasterio.uint8,
        nodata=255,
        crs=crs,
        count=3)
    
    print(kwargs3band)
    print('\n')

    with rasterio.open(out + '\\%s_NIR_G_R_avg50_scaled(0_255).tif'%name, 'w', **kwargs3band) as dst:
        dst.write_band(1, NIR_scaled.astype(rasterio.uint8))
        dst.write_band(2, green_scaled.astype(rasterio.uint8))
        dst.write_band(3, red_scaled.astype(rasterio.uint8))
        
    
    ras.close()

























