from rest_framework import serializers
from .models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # shows username
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())


    class Meta:
        model = Post
        fields =  ['id', 'title', 'content', 'image', 'created_at', 'author', 'category']
