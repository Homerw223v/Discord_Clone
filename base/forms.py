from .models import Room, UserModel
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class UserProfileUpdate(ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'name', 'bio', 'profile_image']


class UserFormCreation(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = UserModel
        fields = ['name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and UserModel.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('This email address is already in use')
        return email


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
