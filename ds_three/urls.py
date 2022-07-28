from django.urls import path , include
from . import views 

urlpatterns = [
    path('', views.chart2, name='chart2'),
    path('line', views.line, name='line'),
    
    
    
]