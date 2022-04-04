from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=8)

class RoadsideCallout(models.Model):
    username = models.CharField(max_length=25)
    status = models.CharField(max_length=10)
    location = models.TextField()
    description = models.TextField()
    mechanic = models.CharField(max_length=25, default='')
    date = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    review = models.TextField(default='')

class UserSubscriptions(models.Model):
    #this could eventually be updated to foreign key and list in user
    username = models.CharField(max_length=25)
    vehicle_registration = models.CharField(max_length=8)
    active = models.BooleanField()