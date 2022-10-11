from django.urls import path , include
from . import views 
from ds_three import views , wrs_app_dash

urlpatterns = [
    # path('', views.chart2, name='chart2'),
    path('funtion_line', views.funtion_line, name='funtion_line'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    
    
    
]