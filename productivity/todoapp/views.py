import json
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from .models import User, Todos, Finished, AllFolders
# Create your views here.
LVLS = (
    ("URGENT", "URGENT"),
    ("NOT URGENT", "NOT URGENT"),
    ("Next Week", "Next Week"),
    ("Next Month", "Next Month"),
    ("In few days", "In few days"),
)

#form
class TodoForm(forms.Form):
    title = forms.CharField(max_length=64)
    notes = forms.CharField(max_length=100)
    dueDate = forms.ChoiceField(choices=LVLS)

class FolderForm(forms.Form):
    title = forms.CharField(max_length=64)

def index(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            notes = form.cleaned_data["notes"]
            dueDate = form.cleaned_data["dueDate"]
            all_todos = Todos(title=title, user=request.user, notes=notes, dueDate=dueDate)
            all_todos.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        #delete the specific todo
        info = json.loads(request.body)
        Todos.objects.filter(id=info.get('todoid', '')).delete()
        #add the specific todo to the finished list (title, )
        finished_list = Finished(title=info.get('title', ''), user=request.user, notes=info.get('notes', ''), dueDate=info.get('due', ''))
        finished_list.save()

    return render(request, "todoapp/index.html", {
        "form": TodoForm(),
        "user": request.user,
    })

def urgency(request):
    non_urgent = request.user.todolist.all().filter(dueDate="NOT URGENT")
    urgent = request.user.todolist.all().filter(dueDate="URGENT")
    nextmonth = request.user.todolist.all().filter(dueDate="Next Month")
    nextday = request.user.todolist.all().filter(dueDate="In few days")
    nextweek = request.user.todolist.all().filter(dueDate="Next Week")
    return render(request, "todoapp/urgency.html", {
        "urgent": urgent,
        "nonurgent": non_urgent,
        "nextmonth": nextmonth,
        "nextday": nextday,
        "nextweek": nextweek
    })

def performance(request):
    todos_finished = request.user.finished_list.all().count()
    not_done = request.user.todolist.all().count()
    score = todos_finished / (not_done)
    tasks = request.user.finished_list.all()
    msg = ""
    if score < 5 and score != 1:
        msg = "Hey! We need to see some more work!"
    elif score > 5 and score < 7 and score != 1:
        msg = "Hmm, decent work done but still some more to go!"
    else:
        msg = "Great work so far!"
        score = 100

    return render(request, "todoapp/performance.html", {"score": score, "msg": msg, "tasks": tasks})

def all_folders(request):
    #create new folders
    #add todos to each folders 
    #click on the folders and u can see all the todos inside that folder
    if request.method == "POST":
        form = FolderForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            folders = AllFolders(title=title, user=request.user)
            folders.save()

    all_folders = request.user.folders.all()
    return render(request, "todoapp/folders.html", {"form": FolderForm(), "folders": all_folders})

def specific_folder(request, name):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        info = json.loads(request.body)
        title = info.get('title', '')
        #somehow get the todo names
        Todos.objects.all().filter(title=title).update(folder=name)
    # todo = Todos.objects.all().get(pk=id)
    todos = Todos.objects.all().filter(folder=name)
    # print(todo.dueDate)
    #either .add() or create urls to save todos into each folder
    return render(request, "todoapp/folder_view.html", {"todos": todos})

def send(request):
    #filter user by username
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        info = json.loads(request.body)
        task = info.get('task', '')
        user = User.objects.get(username__iexact=info.get('username', ''))
        note = info.get('note', '')
        date = info.get('date', '')
        all_todos = Todos(title=task, user=user, notes=note, dueDate=date)
        all_todos.save()
    return render(request, "todoapp/send.html", {})

def edit(request, user_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        message = json.load(request)['msg']
        request.user.todolist.all().filter(id=user_id).update(title=message)
        return HttpResponse("Edit success")
    return HttpResponse("Edit failed")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "todoapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "todoapp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "todoapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "todoapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "todoapp/register.html")