#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 00:03:57 2021

modified from:
    https://plotly.com/python/mixed-subplots/

@author: feynman
"""



import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot

import pandas as pd
import numpy as np

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from shapely.geometry import LineString, MultiLineString
import plotly.graph_objects as go # or plotly.express as px


import plotly.express as px
import geopandas as gpd
import json


# read in volcano database data
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/volcano_db.csv",
    encoding="iso-8859-1",
)

# frequency of Country
freq = df
freq = freq.Country.value_counts().reset_index().rename(columns={"index": "x"})

# read in 3d volcano surface data
df_v = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/volcano.csv")


geo_path = "/home/feynman/Planet/Banks_Timeline/Banks_focused.shp"
geodf = gpd.read_file(geo_path)
# geodf = geodf.to_crs(epsg=4326)
# geodf = geodf.to_crs("WGS84")







# using empet code to convert .shp to geoJSON
def shapefile_to_geojson(gdf, index_list, tolerance=0.025):
    # gdf - geopandas dataframe containing the geometry column and values to be mapped to a colorscale
    # index_list - a sublist of list(gdf.index)  or gdf.index  for all data
    # tolerance - float parameter to set the Polygon/MultiPolygon degree of simplification
    # returns a geojson type dict

    geo_names = list(gdf.index) # name of authorities
    geojson = {'type': 'FeatureCollection', 'features': []}
    for index in index_list:
        geo = gdf['geometry'][index].simplify(tolerance)

        if isinstance(geo.boundary, LineString):
            gtype = 'Polygon'
            bcoords = np.dstack(geo.boundary.coords.xy).tolist()

        elif isinstance(geo.boundary, MultiLineString):
            gtype = 'MultiPolygon'
            bcoords = []
            for b in geo.boundary:
                x, y = b.coords.xy
                coords = np.dstack((x,y)).tolist()
                bcoords.append(coords)
        else: pass



        feature = {'type': 'Feature',
                   'id' : index,
                   'properties': {'name': geo_names[index]},
                   'geometry': {'type': gtype,
                                'coordinates': bcoords},
                    }

        geojson['features'].append(feature)
    return geojson


geojsdata = shapefile_to_geojson(geodf, list(geodf.index))
L = len(geojsdata['features'])







# fig = px.choropleth_mapbox(geodf, geojson=geodf.geometry, locations=geodf.index,
#                            center={"lat": 71.909218, "lon": -120.505967},
#                            mapbox_style="stamen-terrain", zoom=9)


# fig.update_layout(
#     mapbox_style="white-bg",
#     mapbox_layers=[
#         {
#             "below": 'traces',
#             "sourcetype": "raster",
#             "sourceattribution": "United States Geological Survey",
#             "source": [
#                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
#             ]
#         }
#       ])
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# Initialize figure with subplots
fig = make_subplots(
    rows=1, cols=2,
    column_widths=[1, 1],
    row_heights=[1],
    specs=[[{"type": "choroplethmapbox", "rowspan": 1}, {"type": "bar"}]]) #,
           # [            None                    , {"type": "surface"}]])

# # Add scattergeo globe map of volcano locations
# fig.add_trace(
#     go.Scattergeo(lat=df["Latitude"],
#                   lon=df["Longitude"],
#                   mode="markers",
#                   hoverinfo="text",
#                   showlegend=False,
#                   marker=dict(color="crimson", size=4, opacity=0.8)),
#     row=1, col=1
# )
#
# geo_path = "/home/feynman/Planet/Banks_Timeline/AOI/banks_timeline_aoi.shp"
# geodf = gpd.read_file(geo_path)
#
fig.add_trace(
    go.Choroplethmapbox(geojson=json.loads(geodf.to_json()),
    # geojson=geojsdata,
                                    locations=[geojsdata['features'][k]['id'] for k in range(L)],
                                    colorscale="Viridis"),
    # fig.update_layout(mapbox_style="light", mapbox_accesstoken=token,
    # mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129}),
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}),
    row=1, col=1
)

fig.update_layout(mapbox_style='stamen-terrain',
                    height = 750,
                    autosize=True,
                    margin={"r":1,"t":1,"l":1,"b":1},
                    paper_bgcolor='#303030',
                    plot_bgcolor='#303030',
                    mapbox=dict(center=dict(lat=71.909218, lon=-120.505967),zoom=6),
                    )

# fig.add_trace(
#     go.Figure(px.choropleth_mapbox(geodf, geojson=geodf.geometry, locations=geodf.index,
#                                 color=geodf.index, center={"lat": 71.909218, "lon": -120.505967},
#                                mapbox_style="open-street-map", zoom=9)),
#     # fig.update_layout(mapbox_style="light", mapbox_accesstoken=token,
#     # mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129}),
#     # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}),
#     row=1, col=1
# )

#########
# trace = go.Choroplethmapbox( z = np.random.randint(10, 75,  size=L), #synthetic data
#                             locations = [geojsdata['features'][k]['id'] for k in range(L)],
#                             colorscale = 'Viridis',
#                             colorbar = dict(thickness=20, ticklen=3),
#                             geojson = geojsdata,
#                             text = regions,
#                             marker_line_width=0.1, marker_opacity=0.7)
# layout = go.Layout(title_text ='UK LAD Choropleth Demo', title_x =0.5, width=750, height=700,
#                    mapbox = dict(center= dict(lat=54, lon=-2),
#                                  accesstoken= mapbox_access_token,
#                                  zoom=3
#                                ))
#
# fig=go.Figure(data=[trace], layout =layout)
##########

# Add locations bar chart
fig.add_trace(
    go.Bar(x=freq["x"][0:10],y=freq["Country"][0:10], marker=dict(color="crimson"), showlegend=False),
    row=1, col=2
)

# Add 3d surface of volcano
# fig.add_trace(
#     go.Surface(z=df_v.values.tolist(), showscale=False),
#     row=2, col=2
# )

# # Update geo subplot properties
# fig.update_geos(
#     projection_type="orthographic",
#     landcolor="white",
#     oceancolor="MidnightBlue",
#     showocean=True,
#     lakecolor="LightBlue"
# )

# # Rotate x-axis labels
# fig.update_xaxes(tickangle=45)

# # Set theme, margin, and annotation in layout
# fig.update_layout(
#     template="plotly_dark",
#     margin=dict(r=10, t=25, b=40, l=60),
#     annotations=[
#         dict(
#             text="Source: NOAA",
#             showarrow=False,
#             xref="paper",
#             yref="paper",
#             x=0,
#             y=0)
#     ]
# )

# fig.show()
# plot(fig)


# fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# print(geojsdata)
fig.update_layout(clickmode='event+select')

# fig.update_traces(marker_size=20)




app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),

    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """),
            html.Pre(id='relayout-data', style=styles['pre']),
        ], className='three columns')
    ])
])


@app.callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@app.callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)

# app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter

if __name__ == '__main__':
    app.run_server(debug=True)
