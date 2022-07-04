from django.contrib import admin 
from .models import App_per_jesse ,CO2 , Csvforheat 

# Register your models here.




@admin.register(Csvforheat)
class CsvforheatAdmin(admin.ModelAdmin):
   list_display=['id','csv']


@admin.register(CO2)
class COAdmin(admin.ModelAdmin):
   list_display=['id','date','average']

@admin.register(App_per_jesse)
class AppAdmin(admin.ModelAdmin):
    list_display=['id','user_name','app_1','app_2','app_3','app_4','app_5','app_6','app_7','app_8']
