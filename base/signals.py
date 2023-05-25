from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,
                               id=instance.id,
                               email=instance.email,
                               username=instance.username)
        print(Profile.objects.get(id=instance.id), 'created')


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    Profile.objects.filter(user=instance).update(
        username=instance.username,
        email=instance.email)
    print(Profile.objects.get(id=instance.id), 'saved')
