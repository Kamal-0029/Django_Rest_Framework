from django.contrib import admin

# Register your models here.
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "due_date", "completed", "assigned_to")  
    search_fields = ("title", "assigned_to__username")  
    list_filter = ("completed", "due_date")             