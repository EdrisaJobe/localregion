from django.shortcuts import render, redirect
from app.models import Search
from app.forms import SearchForm

# parses data from strings and files
import json

# gets the api
import requests

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
    map = {
        'm': m,
        'form': form,
    }
    
    # getting form request type
    return render(request, 'index.html', map)

def about(request):
    
    return render(request, 'about.html')

def currLocation(request):
    
    # getting the users Ip address
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    
    # content which will fetch user IP address and find location
    res = requests.get('http://ip-api.com/json/'+ip_data['ip'])
    location_data_plain = res.text
    location_data = json.loads(location_data_plain)
    return render(request, 'currlocation.html', {'data': location_data})