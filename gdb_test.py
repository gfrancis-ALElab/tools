#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 22:01:27 2021

@author: feynman
"""

import fiona
import geopandas as gpd





g_file = '/home/feynman/DCOP/TKC_Database_MW.gdb'




layers = fiona.listlayers(g_file)

for layer in layers:
    gdf = gpd.read_file(g_file, layer=layer)




