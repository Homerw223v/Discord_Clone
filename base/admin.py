from django.contrib import admin
from .models import Room, Topic, Message, Profile
# Register your models here.

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Profile)
# class RoomAdmin(admin.ModelAdmin):
#     list_display =

