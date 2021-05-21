# -*- coding: utf-8 -*-
"""
Created on Wed May 19 09:56:53 2021


Scripts for downloading from Planet API


@author: Grant Francis
email: gfrancis@uvic.ca
"""



import os
import requests
import sys
from planet import api
import geojson as gj
import datetime

client = api.ClientV1()

# os.environ['PL_API_KEY']=''
# PLANET_API_KEY = os.getenv('PL_API_KEY')

# BASE_URL = "https://api.planet.com/data/v1"

# session = requests.Session()
# ### authenticate session with user name and password, pass in an empty string for the password
# session.auth = (PLANET_API_KEY, "")
# ### make a get request to the Data API
# res = session.get(BASE_URL)


# print(res.status_code)
# # test response

# print(res.text)
# # print response body


aoi_path = r'C:\Users\gfrancis\Documents\Planet\Banks\Training_Library_Banks_40000\AOI\Banks_Island_mosaic_NIR_G_R_AOI.json'



with open(aoi_path) as f:
    geo_file = gj.load(f)
    aoi = geo_file['geometries'][0]


# date1 = datetime.datetime(year=2018, month=3, day=2)
# date2 = datetime.datetime(year=2019, month=3, day=3)
# filt = api.filters.and_filter(api.filters.date_range('aquired', lt=date2))

# build a filter for the AOI
query = api.filters.and_filter(
    api.filters.geom_filter(aoi),
    api.filters.range_filter('clear_percent', gte=99)
    # api.filters.date_range('aquired', gt=date1),
    # api.filters.date_range('aquired', lt=date2),
    # api.filters.range_filter('cloud_cover', 1t=0.00001)
)


# we are requesting PlanetScope 4 Band imagery
item_types = ['REOrthoTile', 'PSScene4Band']
request = api.filters.build_search_request(query, item_types)
# this will cause an exception if there are any API related errors
results = client.quick_search(request)

# items_iter returns an iterator over API response pages
ids = []
for item in results.items_iter(5000):
  # each item is a GeoJSON feature
  # sys.stdout.write('%s\n' % item['id'])
  sys.stdout.write('%s' % item['id'])
  ids.append('%s' % item['id'])




#%%



#####################################################
# Order files
#####################################################
def get_file(r, path, key):
    headers = {
        'Content-Type': 'application/json',
    }


    json = {    
        "aoi": d['config'][0]['config'],
        "targets": [      
             {       
                 "item_id":r['id'],        
                 "item_type":r['item_type'],#"PSScene4Band",        
                 "asset_type": "Analytic"      
             }    ]
    }
    
    # send the 'ship and clip' order
    print('ordering ', r['id'])
    r = requests.post(
        'https://api.planet.com/compute/ops/clips/v1', 
        headers=headers, 
        json=json, 
        auth=(key, '')
    )
    
    print(r.json())
    # check if asset_type exists:
    if 'message' in r.json():
        message = r.json()['message']
        if 'No access to targets' in message:
            print(message)
            return()

    # check image falls within AOI (sometimes it doesn't !?)
    if 'general' in r.json():
        if len(r.json()['general']) >0:
            if 'message' in r.json()['general'][0]:
                if 'AOI does not intersect targets' in r.json()['general'][0]['message']:
                    print('AOI does not intersect targets')
                    return()

    
    # check up on the order, get its states and print it.
    # it will likely still be running
    r3 = requests.get(
        r.json()['_links']['_self'], 
        auth=(key, ''))

    state = r3.json()['state']
    print('Order status: ', state)
    
    # sleeping 60s between checks to avoid annoying the Planet people
    while state == 'running':
        print('Sleeping ...')
        time.sleep(60)
        r3 = requests.get(
            r.json()['_links']['_self'], 
            auth=(key, '')
        )
        state = r3.json()['state']

        print('Order status: ',state)

    # ... when the order has finished, get the download link ...
    url_download = r3.json()['_links']['results'][0]


    # .. get the response for that link ...
    response = requests.get(url_download)

    #and save to a file name built using the order id
    with open( os.path.join(path, r3.json()['id']+'-clips.zip'), 'wb') as f:
        print('Downloading order')
        f.write(response.content) 


for ID in ids:
    print(ID)
# 	get_file(r, path, key)















