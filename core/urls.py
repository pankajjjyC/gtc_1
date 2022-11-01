from django.urls import path
from . import views

urlpatterns = [
    
    path('login',views.login,name='login'),
    path('',views.login,name='login'),   
    
    path('secure',views.secure,name='secure'),    
    path('logout', views.logout ,name='logout'),
    path('forgtpasswrd', views.forgtpasswrd ,name='forgtpasswrd'),    
   
    path('test1', views.test1, name='test1'),  
    path('test2', views.test2, name='test2'),
    
    path('signup_trac', views.signup_trac, name='signup_trac'),    

    
   
]