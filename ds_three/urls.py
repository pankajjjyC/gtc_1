from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart2, name='chart2'),
    
    
]