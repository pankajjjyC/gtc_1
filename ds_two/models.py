from django.db import models

# Create your models here.

class Csv(models.Model):
    csv=models.FileField() 
    class Meta:
        ordering=['id']