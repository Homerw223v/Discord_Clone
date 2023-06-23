from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.FileField(default='default.jpg', upload_to='profile_image', null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=5000, null=True, blank=True, verbose_name='About')
    email = models.EmailField()
    username = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user}'

    def get_absolute_url(self):
        return reverse('user-profile', args=[str(self.user)])


class Topic(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    host = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(Profile, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)  # Save every time when we update
    created = models.DateTimeField(auto_now_add=True)  # Only save when room was created

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'{self.name}'


class Message(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.body[:50]}'

    class Meta:
        ordering = ['-updated', '-created']
