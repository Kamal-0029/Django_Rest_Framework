from django.urls import path
from .views import BlogCreateAPIView, BlogListAPIView, BlogDetailAPIView, BlogUpdateAPIView, BlogDeleteAPIView, CategoryListAPIView,CategoryDetailAPIView,CategoryUpdateAPIView,CategoryDeleteAPIView,CategoryCreateAPIViews

urlpatterns = [
    
    path('blogs/', BlogListAPIView.as_view(), name='blog_list'),
    path('blogs/<int:pk>/', BlogDetailAPIView.as_view(), name='blog_detail'),
    path('blogs/create/', BlogCreateAPIView.as_view(), name='blog_create'),
    path('blogs/<int:pk>/update/', BlogUpdateAPIView.as_view(), name='blog_update'),
    path('blogs/<int:pk>/delete/', BlogDeleteAPIView.as_view(), name='blog_delete'),

    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path("categories/create/", CategoryCreateAPIViews.as_view(), name="category-create"),
    path("categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="category-detail"),
    path("categories/<int:pk>/update/", CategoryUpdateAPIView.as_view(), name="category-update"),
    path("categories/<int:pk>/delete/", CategoryDeleteAPIView.as_view(), name="category-delete"),
    
]
