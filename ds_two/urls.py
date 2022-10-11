from django.urls import path,include
from . import views
from ds_two import views, dash_app_new
urlpatterns = [
    path('ds_two', views.ds_two, name='ds_two'),#ds_two
    path('test', views.test, name='test'),#test
    path('test2', views.test2, name='test2'),#test2
    path('index', views.index, name='index'),
    path('index2', views.index2, name='index2'),
    path('index3', views.index3, name='index3'),
    

    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    
    
    
]