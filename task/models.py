from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.title
    