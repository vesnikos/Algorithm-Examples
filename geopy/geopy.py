# -*- coding: utf-8 -*-
__author__ = 'vesnikos'
__date__ = '24/09/2014'


from geopy.geocoders import Nominatim

geolocator = Nominatim()
location = geolocator.geocode("waterloo")

print location.raw


