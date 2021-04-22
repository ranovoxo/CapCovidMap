from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd


df = pd.read_csv("C:\\Users\\bikes\\Documents\\repo\\CovidMap\\bikesh8\\testDataApril20.csv",
                   dtype={"Geo_FIPS": str})

import plotly.graph_objects as go

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df.Geo_FIPS, z=df.ORG_T040120,
                                    colorscale="Viridis", zmin=0, zmax=12,
                                    marker_opacity=0.5, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=5, mapbox_center = {"lat": 31.000000, "lon": -100.000000})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()