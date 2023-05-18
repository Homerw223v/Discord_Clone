from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserModel(AbstractUser):
    email = models.EmailField(null=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    bio = models.TextField(max_length=2000, null=True)
    profile_image = models.ImageField(null=True, default='default.jpg', upload_to='profile_image')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    host = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(UserModel, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True) #Save every time when we update
    created = models.DateTimeField(auto_now_add=True) #Only save when room was created

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'{self.name}'


class Message(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.body[:50]}'

    class Meta:
        ordering=['-updated', '-created']

