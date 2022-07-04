from django.contrib import admin
from .models import Csv 

@admin.register(Csv)
class CsvAdmin(admin.ModelAdmin):
   list_display=['id','csv']


# Register your models here.
