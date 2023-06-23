from rest_framework.serializers import ModelSerializer
from ..models import Room, Profile, Topic


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ('host', 'name', 'description', 'updated', 'created')


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'