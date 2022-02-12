from django.shortcuts import render, redirect
from django.http import HttpResponse
from urllib import request
from app.models import Search
from app.forms import SearchForm

import json

# to display map
import folium
# turns a locaiton description into a precise map location
import geocoder
# data visualizer library
import pandas as pd

# Create your views here.
def index(request):
    
    # when useer hits submit, post he following from forms.py
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SearchForm()
    
    # open street map and geocoder link to get a specific location
    address = Search.objects.all().last()
    location = geocoder.osm(address)
    lat = location.lat
    lon = location.lng
    country = location.country
    
    if lat == None or lon == None:
        address.delete()
        return redirect('/')
        
    # making a map object to display on the index page
    # we then represent the map as HTML
    m = folium.Map(location=[lat,lon], zoom_start=15)
    
    # making a custom marker
    folium.Marker([lat,lon],popup=country,icon=folium.Icon(color="blue",icon="info-sign"),).add_to(m)

    
    # gets HTMl representation of map object
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
    }
    
    # getting form request type
    return render(request, 'index.html', context)