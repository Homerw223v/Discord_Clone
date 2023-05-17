from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm


# Create your views here.

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    return render(request, 'login_register/login.html', context={
        'page': page,
    })


def logout_user(request):
    logout(request)
    return render(request, 'login_register/logout.html')


def register_user(requset):
    form = UserCreationForm()
    if requset.method == 'POST':
        form = UserCreationForm(requset.POST)
        if form.is_valid():
            form.save()
            messages.success(requset, f'User {requset.POST.get("username")} was created!')
            return redirect('login')
        else:
            messages.error(requset, 'An error occurred during registration')

    return render(requset, 'login_register/login.html', context={
        'form': form,
    })

def user_profile(request, pk):
    user = User.objects.get(username=pk)
    rooms = user.room_set.all()
    r_messages = user.message_set.all()
    topics = Topic.objects.all()
    return render(request, 'base/profile.html', context={
        'user': user,
        'rooms': rooms,
        'r_messages': r_messages,
        'topics': topics,

    })

def home(request):
    if request.GET.get('q'):
        q = request.GET.get('q')
    else:
        q = ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    r_messages = Message.objects.all().filter(Q(room__topic__name__icontains=q))
    return render(request, 'base/home-page.html', context={
        'rooms': rooms,
        'topics': topics,
        'rooms_count': room_count,
        'r_messages': r_messages,
    })


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')  # Get messages specific only for this room
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    return render(request, 'base/room.html', context={
        'room': room,
        'r_messages': room_messages,
        'participants': participants,
    })


@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            form.save()
            return redirect('home')

    return render(request, 'base/form_for_room.html', context={
        'form': form
    })


@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/form_for_room.html', context={
        'form': form,
    })


@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context={
        'obj': room,
    })

@login_required(login_url='/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        message.delete()
        return redirect('room', message.room.id)
    return render(request, 'base/delete.html', context={
        'message': message,
    })
