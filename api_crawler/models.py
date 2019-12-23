from django.db import models

# Create your models here.
class Apidata (models.Model):
    
    sex = models.CharField(max_length=200, null=True, blank=True)
    height = models.CharField(max_length=200, null=True, blank=True)
    start_weight = models.CharField(max_length=200, null=True, blank=True)
    end_weight = models.CharField(max_length=200, null=True, blank=True)
    total_time = models.CharField(max_length=200, null=True, blank=True)
    age = models.CharField(max_length=200, null=True, blank=True)
    post_id = models.CharField(max_length=200, null=True, blank=True)
    image_sources =  models.CharField(max_length=200, null=True, blank=True)