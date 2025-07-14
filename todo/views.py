from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

@login_required(login_url='/login/')
def index(request):
    # ✅ Extra safety check (optional, but safe)
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due_date")
        description = request.POST.get("description")
        priority = request.POST.get("priority")

        if title:
            Task.objects.create(
                title=title,
                due_date=due_date,
                description=description,
                priority=priority,
                user=request.user
            )
        return redirect("index")

    # ✅ This line is where the error was triggered if user was anonymous
    tasks = Task.objects.filter(user=request.user)
    return render(request, "todo.html", {"tasks": tasks})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/login/')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.completed = not task.completed
        task.save()
    return redirect('index')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
    return redirect('index')


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in automatically
            return redirect('index')  # Redirect to your task list page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})