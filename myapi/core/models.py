from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=8)

class RoadsideCallout(models.Model):
    username = models.CharField(max_length=25)
    status = models.CharField(max_length=10)
    location = models.TextField()
    mechanic = models.CharField(max_length=25, default='')
    date = models.DateField(auto_now_add=False)
    rating = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    review = models.TextField(default='')