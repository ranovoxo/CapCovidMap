import pandas as pd
import geopandas as gpd 
import matplotlib.pyplot as plt
##from shapely.geometry import Point, Polygon

counties = gpd.read_file('counties.geojson')
print(counties.head())

counties.plot()
plt.show()
