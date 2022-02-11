from django.shortcuts import render
from urllib import request
import json

# to display map
import folium
# turns a locaiton description into a precise map location
import geocoder
# data visualizer library
import pandas as pd

# Create your views here.
def index(request):
    
    # open street map and geocoder link to get a specific location
    location = geocoder.osm('New York')
    lat = location.lat
    lon = location.lng
    country = location.country
    
    # making a map object to display on the index page
    # we then represent the map as HTML
    m = folium.Map([lat,lon], zoom_start=50)
    
    # making a custom marker
    folium.Marker([lat,lon],popup=country,icon=folium.Icon(color="blue",icon="info-sign"),).add_to(m)
    
    # gets HTMl representation of map object
    m = m._repr_html_()
    context = {
        'm': m,
    }
    
    
    
    # getting form request type
    return render(request, 'index.html', context)