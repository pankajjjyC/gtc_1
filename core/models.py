from asyncio.windows_events import NULL
from statistics import mode
from django.db import models
from django.contrib.auth.models import User


from django.db.models.signals import pre_save
from django.dispatch import receiver
import os

# Create your models here.
from django.db import models
from sqlalchemy import null, true

# Create your models here.





class Csv_for_heat(models.Model):#used    
    id = models.IntegerField(primary_key=True)
    csv=models.FileField() 



class Csv_score_downld(models.Model):#used
    csv=models.FileField() 


class Identification_model(models.Model):#used
    csv=models.FileField() 


class Permissions(models.Model):
    user_name=models.OneToOneField(User,on_delete=models.CASCADE)
    app_1=models.BooleanField(default=False)
    app_2=models.BooleanField(default=False)
    app_3=models.BooleanField(default=False)
    app_4=models.BooleanField(default=False)
    app_5=models.BooleanField(default=False)
    app_6=models.BooleanField(default=False)
    app_7=models.BooleanField(default=False)
    app_8=models.BooleanField(default=False)     
    class Meta:
        ordering=['id']



class text(models.Model):
    id = models.IntegerField(primary_key=True)
    text=models.CharField(max_length=60)#this is dropdown selected on heatmap3.html saved to database
    battery_voltage=models.CharField(max_length=60,null=True,default=NULL)
    battery_current=models.CharField(max_length=60,null=True,default=NULL)
    no_of_operational=models.CharField(max_length=60,null=True,default=NULL)
    cut_off_thresold=models.CharField(max_length=60,null=True,default=NULL)
    remove_first_col=models.CharField(max_length=60,null=True,default=NULL)
    


class user_details(models.Model):    
    name = models.CharField(max_length=60,null=False, blank=True)
    email=models.CharField(max_length=60)
    reason = models.TextField(max_length=500)
    block_no=models.CharField(max_length=500)


