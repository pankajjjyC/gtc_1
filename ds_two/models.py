from django.db import models

# Create your models here.

class Csv(models.Model):
    csv=models.FileField(upload_to="",default=None) 
    class Meta:
        ordering=['id']