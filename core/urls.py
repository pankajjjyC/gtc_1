from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login',views.login,name='login'),
    path('signup', views.signup,name='signup'),
    path('secure',views.secure,name='secure'),
    path('logout', views.logout ,name='logout'),
    #path('chart', views.chart, name='chart'),
    path('chart', views.chart, name='chart'),
    
    
    #path('index_three',views.index_three,name='index_three'),
    # path('index_four',views.index_four,name='index_four'),
    # path('index_five',views.index_five,name='index_five'),
    # path('index_six',views.index_six,name='index_six'),
    # path('index_seven',views.index_seven,name='index_seven'),
    # path('index_eight',views.index_eight,name='index_eight'),
    
]