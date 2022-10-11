from django.shortcuts import render , HttpResponse
import sys
import os

sys.path.append('C:\\Users\\pankaj\\Desktop\\GTC running app files\\git clone 2 copy\\django-plotly-integration\\ds_three')
#import Paragon_WRS as wrs
# from .Aradiss.abstraction import data
# from .Aradiss.abstraction import correlations
#path = os.getcwd()

def funtion_line(r):
    return render(r, 'ds_three.html') 