#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 20:56:01 2021

@author: feynman
"""


import matplotlib.pyplot as plt
import netCDF4 as nc



file = '/opt/globsim/examples/Example1/era5/era5_pl_20170701_to_20170702.nc'
data = nc.Dataset(file)





plt.imshow(data['t'][0,0,:,:])
