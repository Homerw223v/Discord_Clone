from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Room, Topic, Message, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RoomForm, UserFormCreation, ProfileUpdate, UserUpdate
from django.db.models import ObjectDoesNotExist


# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            Profile.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, 'User does not exist')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username or password does not exist')
    return render(request, 'login_register_reset/login.html')


def logout_user(request):
    logout(request)
    return render(request, 'login_register_reset/logout.html')


def register_user(request):
    form = UserFormCreation()
    if request.method == 'POST':
        form = UserFormCreation(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {request.POST.get("username")} was created!')
            return redirect('user-profile', request.POST.get('username'))
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'login_register_reset/register.html', context={
        'form': form,
    })


@login_required(login_url='login')
def user_profile(request, pk):
    profile = Profile.objects.get(username=pk)
    rooms = profile.room_set.prefetch_related('participants').select_related('host', 'topic')
    r_messages = profile.message_set.all().select_related('user', 'room')
    topics = Topic.objects.select_related('user').prefetch_related('room_set')
    return render(request, 'base/profile.html', context={
        'profile': profile,
        'rooms': rooms,
        'r_messages': r_messages,
        'topics': topics,
    })


@login_required(login_url='login')
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    profile_form = ProfileUpdate(instance=profile)
    user_form = UserUpdate(instance=request.user)
    if request.method == 'POST':
        if request.FILES:
            profile.profile_image.delete()
            file_name = request.FILES.get('profile_image').name.split('.')
            request.FILES.get('profile_image').name = f'{profile.username}_profile_image.{file_name[1]}'
        profile_form = ProfileUpdate(request.POST,
                                     request.FILES,
                                     instance=request.user.profile)
        user_form = UserUpdate(request.POST,
                               instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            profile.profile_image.name = f'{profile.username}_profile_image'
            messages.success(request, 'Information has been updated!')
            return redirect('user-profile', request.user)
    return render(request, 'base/update_profile.html', context={
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile

    })


@login_required(login_url='/login')
def home(request):
    q = ''
    if request.GET.get('q'):
        q = request.GET.get('q')
    rooms = Room.objects.select_related('host', 'topic').prefetch_related('participants').filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.select_related('user').prefetch_related('room_set')
    profile = Profile.objects.get(user=request.user)
    r_messages = Message.objects.select_related('user', 'room').filter(Q(room__topic__name__icontains=q))
    return render(request, 'base/home-page.html', context={
        'rooms': rooms,
        'topics': topics,
        'profile': profile,
        'r_messages': r_messages,
    })


@login_required(login_url='/login')
def room(request, pk):
    profile = Profile.objects.get(user=request.user)
    one_room = Room.objects.select_related('host', 'topic').prefetch_related('participants').get(id=pk)
    room_messages = one_room.message_set.select_related('user')
    if request.method == "POST":
        Message.objects.create(
            user=profile,
            room=one_room,
            body=request.POST.get('body')
        )
        one_room.participants.add(profile)
        return redirect('room', pk=one_room.id)
    return render(request, 'base/room.html', context={
        'room': one_room,
        'profile': profile,
        'r_messages': room_messages,
    })


@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        topic, created = Topic.objects.get_or_create(name=request.POST.get('topic'), user=profile)
        a = Room.objects.create(
            host=profile,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        if request.user.is_authenticated:
            a.participants.add(profile)
            a.save()

        return redirect('home')

    return render(request, 'base/form_for_room.html', context={
        'form': form,
        'topics': topics,
        'profile': profile
    })


@login_required(login_url='/login')
def update_room(request, pk):
    one_room = Room.objects.get(id=pk)
    form = RoomForm(instance=one_room)
    topics = Topic.objects.select_related('user')
    if request.user.username != one_room.host.username:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        one_room.name = request.POST.get('name')
        one_room.topic = topic
        one_room.description = request.POST.get('description')
        one_room.save()
        return redirect('home')
    return render(request, 'base/form_for_room.html', context={
        'form': form,
        'topics': topics,
        'room': one_room,
    })


@login_required(login_url='/login')
def delete_room(request, pk):
    one_room = Room.objects.get(id=pk)
    profile = Profile.objects.get(username=request.user.username)
    if request.user.username != one_room.host.username:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        one_room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context={
        'obj': one_room,
        'profile': profile
    })


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'base/delete.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'The message was deleted successfully')
        return super(MessageDeleteView, self).form_valid(form)

    def test_func(self):
        message = self.get_object()
        if self.request.user.id == message.user.id:
            return True
        return False
