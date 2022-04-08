"""


This py file determines what clients see when they access website


"""


from django.shortcuts import render, redirect
import os
import folium
from folium import CustomIcon
from ipware import get_client_ip
import urllib, json
from folium.plugins import LocateControl, MarkerCluster
from folium.plugins import MousePosition
import time


# explicit import
from .models import *


# Create your views here.
def home(request):

    shp_dir = os.path.join(os.getcwd(), 'media', 'shp')

    m = folium.Map(location=[2.095368, 107.834810], zoom_start=6, tiles='Stamen Terrain')
    LocateControl().add_to(m)
    style_basin = {'fillColor': '#228B22', 'color': '#228B22'}
    style_river = {'color': 'blue'}
    style_MY = {'color': 'green'}
    style_SG = {'color': 'blue'}
    style_IND = {'color': 'beige'}

    folium.GeoJson('https://gist.githubusercontent.com/heiswayi/81a169ab39dcf749c31a/raw/b2b3685f5205aee7c35f0b543201907660fac55e/malaysia.geojson', name='Malaysia',
                   style_function=lambda x:style_MY, ).add_to(m)

    folium.GeoJson('https://raw.githubusercontent.com/yinshanyang/singapore/master/maps/0-country.geojson', name='Singapore',
                   style_function=lambda y:style_SG, ).add_to(m)

    folium.GeoJson('https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson', name='Indonesia',
                    style_function=lambda z: style_IND, ).add_to(m)


    # folium.GeoJson(os.path.join(shp_dir, 'basin.geojson'), name='basin',
    #                style_function=lambda x:style_basin).add_to(m)
    #
    # folium.GeoJson(os.path.join(shp_dir, 'rivers.geojson'), name='basin',
    #                style_function=lambda y:style_river).add_to(m)


    folium.LayerControl().add_to(m)

    m = m._repr_html_()
    context = {'my_map': m}
    return render(request, 'geoApp/home.html', context)

# introduction
def about(request):
    return render(request, 'geoApp/About.html')

# Second page
def explore(request):
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        client_ip="0.0.0.0"
    else:
        if is_routable:
            ip_type="Public"
        else:
            ip_type="Private"
    ip_address = '106.220.90.88'
    # ip_address = '192.168.0.184'

    try:
        url = 'https://api.ipfind.com/?ip=' + client_ip
        response = urllib.request.urlopen(url)
        data1 = json.loads(response.read())
        longitude=data1["longitude"]
        latitude=data1["latitude"]
    except:
        url = 'https://api.ipfind.com/?ip=' + ip_address
        response = urllib.request.urlopen(url)
        data1 = json.loads(response.read())
        longitude=data1["longitude"]
        latitude=data1["latitude"]


    m = folium.Map(location=[latitude,longitude],zoom_start=5,)

    LocateControl(auto_start=True, zoom_start=5,
                  strings={'title': 'See you current location', 'popup': 'Your position'}).add_to(m)




    MousePosition().add_to(m)
    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"

    MousePosition(
        position="topright",
        separator=" | ",
        empty_string="NaN",
        lng_first=False,
        num_digits=20,
        prefix="Coordinates:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m)


    # icon image
    icon = "http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png"

    icong = folium.CustomIcon(icon, icon_size=(20, 20))

    markerCluster = MarkerCluster(name="Markers Demo").add_to(m)

    for i in df:
        iframe = folium.IFrame(
            'Address:' + str(i[0]) + '<br>' + 'Name: ' + 'McDonald' + '<br>' + 'Latitude: ' + str(
                i[1]) + '<br>' + 'Longitude: ' + str(i[2]))
        popup = folium.Popup(iframe, min_width=300, max_width=300)
        folium.Marker(location=(i[1], i[2]), popup=popup, ).add_to(markerCluster)

    # for i in df:
    #     iframe = folium.IFrame(
    #         'Address:' + str(i[0]) + '<br>' + 'Name: ' + 'McDonald' + '<br>' + 'Latitude: ' + str(
    #             i[1]) + '<br>' + 'Longitude: ' + str(i[2]))
    #     popup = folium.Popup(iframe, min_width=300, max_width=300)
    #     folium.Marker(location=(i[1], i[2]), popup=popup, ).add_to(m)


    m = m._repr_html_()
    context = {'my_map': m}
    return render(request, 'geoApp/Explore.html', context)