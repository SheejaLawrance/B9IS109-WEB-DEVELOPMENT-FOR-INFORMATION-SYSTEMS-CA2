from django.db import models
from django.contrib.auth.models import User
# Create your models 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email_id= models.CharField(max_length=55, unique=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture-973460_1280.png', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    years_of_exp = models.PositiveIntegerField(blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"