from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/<str:pk>/', views.user_profile, name='user-profile'),
    path('', views.home, name='home'),
    path('room/<int:pk>/', views.room, name='room'),
    path('create_room/', views.create_room, name='create-room'),
    path('update-room/<int:pk>/', views.update_room, name='update-room'),
    path('delete-room/<int:pk>/', views.delete_room, name='delete-room'),
    path('delete-message/<int:pk>/', views.MessageDeleteView.as_view(), name='delete-message'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='login_register_reset/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='login_register_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='login_register_reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='login_register_reset/password_reset_complete.html'),
         name='password_reset_complete')
]
