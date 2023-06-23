from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Room, Profile, Topic
from .serializers import RoomSerializer, TopicSerializer
from rest_framework import generics
from rest_framework.views import APIView


@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET api/',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/profiles',
        'GET /api/topics'
    ]
    return Response(routes)


@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_room(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)


class ProfileApiView(APIView):
    def get(self, request):
        lst = Profile.objects.all().values()
        return Response({'profiles': list(lst)})


class TopicAPIView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
