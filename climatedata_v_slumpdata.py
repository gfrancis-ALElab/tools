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
import datetime
from natsort import natsorted
import glob



### input slump data

slumps_file = '/home/feynman/Planet/Banks_Timeline/Focused_Regions/Priority_20thresh_10buffer.shp'
slumps = gpd.read_file(slumps_file)
slumps['center_utm'] = slumps.centroid
zn = int(slumps.crs.name[-3:-1])
zl = slumps.crs.name[-1]
c = utm.to_latlon(slumps['center_utm'][:].x, slumps['center_utm'][:].y, zn, zl)
slumps['center_lat_lon'] = list(zip(*c))

### example nc file for coordinate grid conversion
climate_files_dir = '/opt/globsim/examples/Banks_data'
climate_file = climate_files_dir + '/era5/era5_rea_pl_20120622_to_20120623.nc'
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

def get_timeseries(var, grid_lat, grid_lon):
    
    if var in ['t', 'r', 'u', 'v', 'z']:
        atype = 'pl'
    elif var in ['t2m', 'd2m', 'u10', 'v10', 'tco3', 'tcwv']:
        atype = 'sa'
    elif var in ['tp', 'ssrd', 'strd']:
        atype = 'sf'
    else:
        raise ValueError('variable not recognized')


    series = []
    timeFULL = []
    for ncfile in natsorted(glob.glob(climate_files_dir + '/era5/*%s*.nc'%atype)):
        
        nc_data = nc.Dataset(ncfile)
        ### convert netCDF4 time hours since 1900 01 01 to readable time
        time = nc.num2date(nc_data['time'],
                            nc_data['time'].units,
                            nc_data['time'].calendar,
                            only_use_cftime_datetimes=False)
        
        if atype == 'pl':
### pressure levels: [ 750,  775,  800,  825,  850,  875,  900,  925,  950, 975, 1000]
            try:
                series.extend(nc_data[var][:,-1,grid_lat,grid_lon])
                timeFULL.extend(time)
            except: pass
        else:
            try:
                series.extend(nc_data[var][:,grid_lat,grid_lon])
                timeFULL.extend(time)
            except: pass
    
    label = nc_data[var].long_name
    units = nc_data[var].units
    
    return series, timeFULL, label, units




# fig, ax1 = plt.subplots(figsize=(20,10))
# ax2 = ax1.twinx()
# for variable in ['t','t2m','d2m']:
#     series, time, label, units = get_timeseries(variable, 4, 8)
#     ax1.plot(time, series, label='%s [%s]'%(label,units))
# series, time, label, units = get_timeseries('tp', 4, 8)
# ax2.plot(time, series, color='purple', label='%s [%s]'%(label,units))


# fig.legend()
# plt.xlabel('Time [YYY-MM-DD]')
# plt.tight_layout()
# plt.savefig('climate_data_grid0408.svg', format="svg")





variables = ['t', 'r', 'u', 'v', 'z',
              't2m', 'd2m', 'u10', 'v10', 'tco3', 'tcwv',
              'tp', 'ssrd', 'strd']


df = pd.DataFrame()
series, time, label, units = get_timeseries('t', 3, 11)
df['time'] = time
df[label + ' [%s]'%units] = series

df2 = pd.DataFrame()


length = 0
for variable in variables:
    series, time, label, units = get_timeseries(variable, 3, 11)
    # d = {'time': time, label: series}
    
    if len(time) == len(df['time']):
        df[label + ' [%s]'%units] = series
    
    else:
        if 'time' in df2:
            df2[label + ' [%s]'%units] = series
        else:
            df2['time'] = time
            df2[label + ' [%s]'%units] = series

# print(df)
# print(df2)



df.to_csv('Banks_ERA5_grid0311.csv')
# df2.to_csv('WR_ERA5_set2_grid0408.csv')
slumps.to_csv('Banks_slumps_ERA5_crossinfo.csv',
              columns = ['Id', 'center_utm', 'center_lat_lon', 'grid_index'])













### structure for pl data (level=1000 for surface)
### t,r,u,v,z(time, level, lat, lon)
# essentially need this: (nc_data['_'][:,level,lat,lon])


### label = nc_data['_'].standard_name
### units = nc_data['_'].units


### structure for pl data
### (time, level, lat, lon)


### structure for sa data
### t2m, d2m, u10, v10, tco3, tcwv(time, latitude, longitude)


### structure for sf data (total precip, Surface solar radiation downwards,
###                         Surface thermal radiation downwards)
### tp, ssrd, strd(time, latitude, longitude)

















