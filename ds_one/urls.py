from django.urls import path ,include
from . import views
from ds_one import simpleexample

urlpatterns = [
    path('', views.chart, name='chart'),
    path('chart_dsone', views.chart_dsone, name='chart_dsone'),
    path('watchdemo', views.watchdemo, name='watchdemo'),
    path('sample2', views.sample2, name='sample2'),
    path('samplesave', views.samplesave, name='samplesave'),
    path('charts', views.charts, name='charts'),
    path('sample3', views.sample3, name='sample3'),
    path('chart1', views.chart1, name='chart1'),
    path('chart2', views.chart2, name='chart2'),
    path('chart_step2', views.chart_step2, name='chart_step2'),
    path('chart_step3', views.chart_step3, name='chart_step3'),
    path('chart_step4', views.chart_step4, name='chart_step4'),

    path('iden', views.iden, name='iden'),
    path('venue', views.venue, name='venue'),
    
    path('trial',views.trial,name='trial'),
    path('try1',views.try1,name='try1'),
    path('try2',views.try2,name='try2'),

    

    
     
]