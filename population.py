#------------------------------------------------------------------
# Developer ----- Bryce Martin 
# Description --- This program will produce a webmap with folium
#                 and read data of volcanos within USA with pandas.
# 
#------------------------------------------------------------------
import folium
from folium.map import FeatureGroup
import pandas

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Stamen Terrain")

#pandas function to read in files
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elevation = list(data["ELEV"])

#a function to determin marker colors based on volcano height.
def marker_color(e):
    if e >= 0  and e <= 1500:
        return "green"
    elif e > 1500 and e <= 2300:
        return "orange"
    else:
        return "red"

#to add objects to the "map" object we can use markers/elements with built in functions in folium
fgv= folium.FeatureGroup(name = "Volcanoes")

# the zip function lets us iterate through both lists at the same time
for lt,ln,el in zip(lat,lon, elevation):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], fill = True, radius= 6, popup= str(el) + "m", fill_color=marker_color(el), color = "black", fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

#adding to feature group
#GeoJson is a special case of json file. It contains a dictionary with keys/values
#our file contains the coordinates of different countries and makes them individual polygons
# a lambda function with  name that specifies anythin and creats a function in a single line
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding= 'utf-8-sig').read(), 
style_function= lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

 #adding layer control (option to toggle what layers we see)

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")