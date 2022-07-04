from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('ds_two', include('ds_two.urls')),
    path('ds_three', include('ds_three.urls')),
]
