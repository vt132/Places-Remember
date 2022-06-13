from django.db import models
from mapbox_location_field.models import LocationField  
from django.contrib.auth.models import User

class Memories(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    position = LocationField() 
    desc =models.CharField(max_length=1000, null=False)
