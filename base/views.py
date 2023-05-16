from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm


# Create your views here.

def home(request):
    rooms = Room.objects.all
    return render(request, 'base/home-page.html', context={
        'rooms': rooms,
    })


def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'base/room.html', context={
        'room': room,
    })


def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/form_for_room.html', context={
        'form': form
    })

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/form_for_room.html', context={
        'form': form,
    })

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect(room)
    return render(request, 'base/delete.html', context={
        'obj': room,
    })
