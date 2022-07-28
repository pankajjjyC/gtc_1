from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart, name='chart'),
    path('watchdemo', views.watchdemo, name='watchdemo'),
    path('sample2', views.sample2, name='sample2'),
     
]