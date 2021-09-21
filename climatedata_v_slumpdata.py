#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 20:56:01 2021

@author: feynman
"""

import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import geopandas as gpd
import pandas as pd
import utm



### input data

slumps_file = '/home/feynman/Planet/WR_Timeline/Priority_Regions/Priority_20thresh_8buffer.shp'
slumps = gpd.read_file(slumps_file)
slumps['center_utm'] = slumps.centroid
c = utm.to_latlon(slumps['center_utm'][:].x, slumps['center_utm'][:].y, 8, 'N')
slumps['center_lat_lon'] = list(zip(*c))

climate_file = '/opt/globsim/examples/WR_data/era5/era5_rea_sa_20200531_to_20200601.nc'
nc_data = nc.Dataset(climate_file)


### get netcdf grid index for each slump based on lat lon of slump

indices = []
for point in slumps['center_lat_lon']:
    
    cy = point[0]
    cx = point[1]

    lat = float(min(nc_data['latitude'], key=lambda x:abs(x-cy)).data)
    lat_index = list(nc_data['latitude'][:].data).index(lat)
    
    lon = float(min(nc_data['longitude'], key=lambda x:abs(x-cx)).data)
    lon_index = list(nc_data['longitude'][:].data).index(lon)
    
    indices.append(tuple((lat_index, lon_index)))

    
slumps['grid_index'] = indices


Ids_loc = slumps['grid_index']
Ids_loc = pd.DataFrame(Ids_loc)
Ids_loc.insert(0, 'Id', Ids_loc.index)



### create time series of a variable given grid index



### structure for pl data
### (time, level, lat, lon)
# plt.imshow(data['u'][0,0,:,:])





### convert netCDF4 time hours since 1900 01 01 to readable time
# nc.num2date(data['time'], data['time'].units, data['time'].calendar)



