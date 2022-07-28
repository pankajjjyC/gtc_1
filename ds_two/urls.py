from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart1, name='chart1'),#ds_two
    path('bar', views.bar, name='bar'),
    
    
]