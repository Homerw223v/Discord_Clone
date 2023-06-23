from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('roomlist', views.get_rooms),
    path('room/<str:pk>', views.get_room),
    path('profilelist/', views.ProfileApiView.as_view()),
    path('topiclist/', views.TopicAPIView.as_view())
]
