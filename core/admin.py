from django.contrib import admin 
from .models import Permissions ,text, user_details, Identification_model , Csv_score_downld , Csv_for_heat 
# Register your models here.




@admin.register(Csv_for_heat)
class Csv_for_heatAdmin(admin.ModelAdmin):
   list_display=['id','csv']



@admin.register(Identification_model)
class Identification_modelAdmin(admin.ModelAdmin):
   list_display=['id','csv']

@admin.register(Csv_score_downld)
class Csv_score_downld_Admin(admin.ModelAdmin):
   list_display=['id','csv']


@admin.register(Permissions)
class AppAdmin(admin.ModelAdmin):
    list_display=['id','user_name','app_1','app_2','app_3','app_4','app_5','app_6','app_7','app_8']


@admin.register(text)
class textAdmin(admin.ModelAdmin):
   list_display=['id','text']

@admin.register(user_details)
class userdetailsAdmin(admin.ModelAdmin):
   list_display=['id','name','email','reason','block_no']