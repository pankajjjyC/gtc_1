from django.contrib import admin
from .models import Csvforbar 

@admin.register(Csvforbar)
class CsvforbarAdmin(admin.ModelAdmin):
   list_display=['id','csv']
