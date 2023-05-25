from django.contrib.auth.models import User

from .models import Room, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserUpdate(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'profile_image']


class UserFormCreation(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and Profile.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('This email address is already in use')
        return email


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
