#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 20:56:01 2021

@author: feynman
"""


import matplotlib.pyplot as plt
import netCDF4 as nc



file = '/opt/globsim/examples/WR_data/era5/era5_rea_pl_20200531_to_20200601.nc'
data = nc.Dataset(file)





plt.imshow(data['t'][0,0,:,:])
