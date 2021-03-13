from django import forms
from common.models import UserProfile
from django.conf import settings

class ProfileCreationForm(forms.Form):
    
    age = forms.IntegerField()
    sex = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)