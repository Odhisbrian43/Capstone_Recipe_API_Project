from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user extended from abstractuser class with extra fields.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, unique=True)

#A string representation of the CustomUser class.
    def __str__(self):
        return f"{self.username}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)# Delete profile when user is deleted.
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    postal_code = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='profile_pic')

#How the profile will be presented.
    def __str__(self):
        return f'{self.user.username} Profile'




