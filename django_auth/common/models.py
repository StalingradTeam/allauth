from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount


# Create your models here.

class UserProfile(models.Model):

    age = models.IntegerField()
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username