#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 16:41:48 2021

tool for creating .CSV list of stations for Globsim download

stations lat & lon from ENVIRONMENT CANADA
elevation from NRCAN

@author: gfrancis
"""


import pandas as pd
from pykml import parser
import urllib
import json


def get_elevation(lat, lon):

    server = 'http://geogratis.gc.ca/services'
    url = server + '/elevation/cdsm/altitude?lat=%s&lon=%s'%(lat, lon)
    
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        page = res.read().decode()
    res.close()
    literal = page.replace('\r\n', '')
    d = json.loads(literal)
    
    return d['altitude']



kfile = '/home/feynman/station_list.kml'

# get site names & coordinates
with open(kfile) as f:
    kdoc = parser.parse(f).getroot().Document.Folder

nums = []
stations = []
lats = []
lons = []
elevations = []
count = 1
for place in kdoc.Placemark:
    nums.append(count)
    stations.append(str(place.name))
    lon = float(str(place.Point.coordinates).replace('\n','').split(',')[0])
    lons.append(lon)
    lat = float(str(place.Point.coordinates).replace('\n','').split(',')[1])
    lats.append(lat)
    # get elevation if available from NRCAN
    elevations.append(get_elevation(lat, lon))
    count += 1

info = {'station_number':nums, 'station_name':stations, 'longitude_dd':lons,
        'latitude_dd':lats, 'elevation_m':elevations}


#%%

# save full list
station_data = pd.DataFrame(data=info)
station_data.to_csv('/home/feynman/env_can_station_list.csv', index=False)


# save sites within bounding box
N = 69
S = 67
W = -137.5
E = -132.5

filtered_station_list = station_data[(station_data['latitude_dd'] < N)
                                     & (station_data['latitude_dd'] > S)
                                     & (station_data['longitude_dd'] < E)
                                     & (station_data['longitude_dd'] > W)]
filtered_station_list = filtered_station_list.reset_index(drop=True)
filtered_station_list['station_number'] = filtered_station_list.index + 1


filtered_station_list.to_csv('/home/feynman/WR_sitelist.csv', index=False)















