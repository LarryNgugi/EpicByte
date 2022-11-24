from django.db import models


# Create your models here.

class Dashboard(models.Model):
    cost = models.CharField(max_length=500,blank=True,null=True)

