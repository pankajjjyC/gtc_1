from django.urls import path ,include
from . import views
from ds_one import simpleexample


urlpatterns = [
    path('', views.chart, name='chart'),
    
    path('watchdemo', views.watchdemo, name='watchdemo'),
    path('sample2', views.sample2, name='sample2'),
    path('samplesave', views.samplesave, name='samplesave'),
    path('charts', views.charts, name='charts'),
    path('sample3', views.sample3, name='sample3'),
    path('chart1', views.chart1, name='chart1'),
    path('chart2', views.chart2, name='chart2'),  
    
    path('chartdetection', views.chartdetection, name='chartdetection'),
    path('chartdetection2', views.chartdetection2, name='chartdetection2'),
    path('chartdetection3', views.chartdetection3, name='chartdetection3'),

    path('chartdetection_mlper', views.chartdetection_mlper, name='chartdetection_mlper'),
    path('chartdetection_mlper2', views.chartdetection_mlper2, name='chartdetection_mlper2'),
    path('chartdetection_mlper3', views.chartdetection_mlper3, name='chartdetection_mlper3'),

    path('chartsdetection_inject_ano', views.chartsdetection_inject_ano, name='chartsdetection_inject_ano'),
    path('chartsdetection_detec_perfor', views.chartsdetection_detec_perfor, name='chartsdetection_detec_perfor'),

    path('saveanamolies', views.saveanamolies, name='saveanamolies'),  
    
    path('venue', views.venue, name='venue'),   
    
    path('pdf2', views.pdf2, name='pdf2'),    
    
    path('try2',views.try2,name='try2'),    
  
]