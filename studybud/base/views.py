from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Create your views here.

def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'email or password does not exisits.')
    
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def registerPage(request):
    form = MyUserCreationForm()
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # commit = False so we can make the username in lowercase before saving it
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'An error occured during registeration.')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)
    

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')
    

def home(request):
    topic = request.GET.get('topic') or ''
    search = request.GET.get('search') or ''
    activities = Message.objects.filter( Q(room__topic__name__icontains=topic) )[:10]
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=topic) & (Q(topic__name__icontains=search) | 
        Q(name__icontains=search) | Q(description__icontains=search) | Q(topic__name__icontains=search))
    )
    topics = Topic.objects.all()[:8]
    
    context = {'rooms': rooms, 'topics': topics, 'activities': activities}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get('body')
        )
        if request.user not in participants:
            joinRoom(request, room.id)
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context) 


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    activities = user.message_set.all()
    topics = Topic.objects.all()
    
    context = {'user': user, 'rooms': rooms, 'activities': activities, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics}
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, _ = Topic.objects.get_or_create(name=topic_name)
             
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
        
        # if form.is_valid:
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse('You are not Allowed here!')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, _ = Topic.objects.get_or_create(name=topic_name)
    
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def joinRoom(request, pk):    
    Room.objects.get(id=pk).participants.add(request.user)
    return redirect('room', pk=pk)


@login_required(login_url='login')
def leaveRoom(request, pk):
    Room.objects.get(id=pk).participants.remove(request.user)
    return redirect('room', pk=pk)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if message.user != request.user:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    
    context = {'form': form}
    return render(request, 'base/update-user.html', context)


def topicsPage(request):
    search = request.GET.get('search') or ''
    print(search)
    topics = Topic.objects.filter( name__icontains=search )
    
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    activities = Message.objects.all()
    
    return render(request, 'base/activity.html', {'activities': activities})