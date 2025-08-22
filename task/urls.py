from django.urls import path
from .views import TaskListAPIView, TaskCreateAPIView, TaskDetailAPIView

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateAPIView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),  # handles GET, PUT, DELETE
    
]
