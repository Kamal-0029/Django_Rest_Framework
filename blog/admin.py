from django.contrib import admin

# Register your models here.
from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")        
    search_fields = ("name",)               

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "created_at")  
    search_fields = ("title", "content")     
    list_filter = ("created_at", "category", "author")  