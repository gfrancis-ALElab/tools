#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 20:56:01 2021

@author: feynman
"""


import matplotlib.pyplot as plt
import netCDF4 as nc
import geopandas as gpd
import utm


file = '/opt/globsim/examples/WR_data/era5/era5_rea_sa_20200531_to_20200601.nc'
nc_data = nc.Dataset(file)

N = max(nc_data['latitude'][:])
S = min(nc_data['latitude'][:])
E = max(nc_data['longitude'][:])
W = min(nc_data['longitude'][:])


slumps_file = '/home/feynman/Planet/WR_Timeline/Priority_Regions/Priority_20thresh_8buffer.shp'
slumps = gpd.read_file(slumps_file)





#### utm.to_latlon(center.x, center.y, 8, 'N')



### structure for pl data
### (time, level, lat, lon)
# plt.imshow(data['u'][0,0,:,:])





### convert netCDF4 time hours since 1900 01 01 to readable time
# nc.num2date(data['time'], data['time'].units, data['time'].calendar)



