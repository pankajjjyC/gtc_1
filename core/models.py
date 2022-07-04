from statistics import mode
from django.db import models
from django.contrib.auth.models import User


from django.db.models.signals import pre_save
from django.dispatch import receiver
import os

# Create your models here.
from django.db import models

# Create your models here.
class CO2(models.Model):
    date = models.DateField()
    average = models.FloatField()

    class Meta:
        ordering = ('date',)



class Csvforheat(models.Model):
    csv=models.FileField() 


    
    


class App_per_jesse(models.Model):
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


