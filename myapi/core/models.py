from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=8)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # Override the save method of the model
    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)

        img = Image.open(self.image.path) # Open image
        
        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image

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
    vehicle_registration = models.CharField(max_length=6)
    vehicle_type = models.CharField(max_length=25)
    vehicle_model = models.CharField(max_length=25)
    vehicle_brand = models.CharField(max_length=25)
    vehicle_year = models.CharField(max_length=25)
    vehicle_weight = models.CharField(max_length=25)
    active = models.BooleanField()

class UserLocation(models.Model):
    username = models.CharField(max_length=25)
    location = models.JSONField() # this is currently latitude and longitude object