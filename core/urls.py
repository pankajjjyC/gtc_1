from django.urls import path
from . import views

urlpatterns = [
    
    path('login',views.login,name='login'),
    path('',views.login,name='login'),
    path('signup', views.signup,name='signup'),
    path('secure',views.secure,name='secure'),
    path('logout', views.logout ,name='logout'),
    
    path('sample', views.sample, name='sample'),
    path('sample2', views.sample2, name='sample2'),
    
    
    
    
]