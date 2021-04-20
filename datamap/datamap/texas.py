import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt 
import plotly
import plotly.figure_factory as ff
import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np
import json
import shapely
##import geojsonio

## Reading in the csv file
def texas_counties():
    counties = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/minoritymajority.csv')
    counties_x = counties[counties['STNAME'] =='Texas']

    values = counties_x['TOT_POP'].tolist()
    fips = counties_x['FIPS'].tolist()
    
    endpts = list(np.mgrid[min(values):max(values):4j])

    ## dropping unnecessary data from counties geodata
    counties_x = counties_x.drop(columns = ["TOT_POP","TOT_MALE", "WA_MALE", "TOT_FEMALE", "WA_FEMALE", 
    "NHWA_MALE", "NHWA_FEMALE", "NHWhite_Alone", "Not_NHWhite_Alone","MinorityMinority","MinorityPCT", "Black", "BlackPCT", "Hispanic", "HispanicPCT" ])
    countycases = gpd.read_file('texasdata.csv')
    data_transposed = countycases.T
    
    ##countycases = countycases.drop([0]) ## get rid of column with number lables
    ##print(merge.head())
  
    
    countycases['Index'] = countycases['Index'].astype(str) + " County"    ## Adding County to each row to help merge
    
    print(countycases.head())
    merge = pd.concat([counties_x, countycases], axis = 1)
    print(merge.head())
    """ Check if both files contain matching counties 
    for index, row in countycases.iterrows():  
       if row[0] + " County" not in counties_x['CTYNAME'].to_list():
            print(row[0] + "not in the list of the file")
       else:
            pass
    """

    ##merge = counties_x.join(countycases, on = 'CTYNAME', how = 'right')
    ##print(counties_x.head())
    ##print(data_transposed.head())
    #counties = counties.to_json()
    colorscale = ["#030512","#1d1d3b","#323268","#3d4b94","#3e6ab0",
              "#4989bc","#60a7c7","#85c5d3","#b7e0e4","#eafcfd"]
    fig = ff.create_choropleth(
        fips=fips, values= values, scope=['Texas'], show_state_data=True,
        colorscale=colorscale, binning_endpoints=endpts, round_legend_values=True,
        plot_bgcolor='rgb(229,229,229)',
        paper_bgcolor='rgb(229,229,229)',
        legend_title='Population by County',
        county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
        exponent_format=True,
    )
    fig.update_layout(
        mapbox_style = 'carto-positron',
        paper_bgcolor = 'rgba(0,0,0,0)',
        mapbox_zoom = 2.75,
        mapbox_center = {'lat': 370902, 'lon': -95.7129},
        margin = dict(t = 0, l=0, r=0, b=0)
    )
    ##fig.layout.template = None
    plot_div = plot(fig, output_type = 'div', config = { 'displayModeBar' : False})

    return plot_div