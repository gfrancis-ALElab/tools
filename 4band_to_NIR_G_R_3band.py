# -*- coding: utf-8 -*-
"""
Created on Mon May 10 15:52:58 2021

@author: gfrancis
"""

import rasterio
import numpy as np




lib = r'C:\Users\gfrancis\Documents\Planet_data\HWC\HWC_aoi_20200808_PSScene4Band_Explorer\files'
name = '20200808_mosaic.tif'
pic = lib + '\\' + name
out = r'C:\Users\gfrancis\Documents\Planet_data\HWC'


ras = rasterio.open(pic)
assert ras.meta['count'] == 4
bandRed = ras.read(3)
bandgreen = ras.read(2)
bandNIR = ras.read(4)

NIR_arr = bandNIR.astype(float)
green_arr = bandgreen.astype(float)
red_arr = bandRed.astype(float)


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
    count=3)


with rasterio.open(out + '\\%s_NIR_G_R.tif'%name, 'w', **kwargs3band) as dst5:
    dst5.write_band(1, NIR_arr.astype(rasterio.uint8))
    dst5.write_band(2, green_arr.astype(rasterio.uint8))
    dst5.write_band(3, red_arr.astype(rasterio.uint8))
    

ras.close()

























