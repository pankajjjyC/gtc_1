from django.urls import path
from . import views

urlpatterns = [
    
    path('login',views.login,name='login'),
    path('',views.login,name='login'),

    path('signup_ara', views.signup_ara,name='signup_ara'),
    path('signup_dis', views.signup_dis,name='signup_dis'),
    path('signup_loc', views.signup_loc,name='signup_loc'),
    path('signup_trac', views.signup_trac,name='signup_trac'),
    path('signup_cas', views.signup_cas,name='signup_cas'),
    path('signup_trat', views.signup_trat,name='signup_trat'),
    
    path('secure',views.secure,name='secure'),
    path('secure_',views.secure_,name='secure_'),
    path('logout', views.logout ,name='logout'),
    path('forgtpasswrd', views.forgtpasswrd ,name='forgtpasswrd'),
    
    path('sample', views.sample, name='sample'),
    path('sample2', views.sample2, name='sample2'),
    path('sample3', views.sample3, name='sample3'),  
    
]