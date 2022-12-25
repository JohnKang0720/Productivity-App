from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class AllFolders(models.Model):
    title = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="folders")

class Todos(models.Model):
    title = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="todolist")
    notes = models.CharField(max_length=100, blank=True)
    dueDate = models.CharField(max_length=100)
    folder = models.CharField(max_length=64, blank=True)

class Urgency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    todos = models.ForeignKey(Todos, on_delete=models.CASCADE, blank=True)

class Performance(models.Model):
    score = models.IntegerField()

class Finished(models.Model):
    title = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="finished_list")
    notes = models.CharField(max_length=100, blank=True)
    dueDate = models.CharField(max_length=100)

