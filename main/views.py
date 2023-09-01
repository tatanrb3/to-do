from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *


def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST['input-username']
    password = request.POST['input-password']

    print(username, password)

    try:
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    except:
        message = "User doesn´t exist, try again"
        return render(request, 'login.html', {
            'message': message
        })


def signup(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    username = request.POST['input-username']
    password1 = request.POST['input-password1']
    password2 = request.POST['input-password2']

    if password1 == password2:
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        login(request, user)
        return redirect('/')
    else:
        message = "Passwords doesn´t match, try again"
        return render(request, 'register.html', {
            'message': message
        })


def signout(request):
    print("Si entró")
    logout(request)

    message = "Session closed"
    print(message)
    return render(request, 'login.html', {
        'message': message
    })


@login_required
def index(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'index.html', {
            'tasks': tasks
        })
    else:
        tarea = request.POST['input_tarea']
        status_in_progress = Status.objects.get(name="In progress")
        task = Task.objects.create(name=tarea, user=request.user, status=status_in_progress)
        task.save()
        return redirect('/')


@login_required
def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('/')


@login_required
def finish_task(request, id):
    status_finished = Status.objects.get(name="Finished")
    task = Task.objects.get(id=id)
    task.status = status_finished
    task.save()
    return redirect('/')
