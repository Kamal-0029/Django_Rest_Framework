from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from .models import Task
from .serializer import TaskSerializer
from django.shortcuts import get_object_or_404

# ✅ View to list tasks for the logged-in user
class TaskListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


# ✅ View to create a new task (with due_date validation)
class TaskCreateAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print("11111111", request.data)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            print("11111111", serializer.validated_data)
            # Validate due_date is in the future
            due_date = serializer.validated_data.get("due_date")
            if due_date and due_date < timezone.now().date():
                return Response(
                    {"error": "Due date must be in the future."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Save task assigned to current user
            serializer.save(assigned_to=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ View to retrieve, update, and delete a task (only if user owns it)
class TaskDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        # Only return task if it's assigned to the logged-in user
        return get_object_or_404(Task, pk=pk, assigned_to=user)

    def get(self, request, pk):
        task = self.get_object(pk, request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk, request.user)
        print("put", task == request.user)
        # Check if logged-in user is the assignee
        if task.assigned_to != request.user:
            return Response(
                {"error": "You are not allowed to update this task."},
                status=status.HTTP_403_FORBIDDEN
            )       
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            # Optional: check due_date again if updated
            due_date = serializer.validated_data.get("due_date")
            if due_date and due_date < timezone.now().date():
                return Response(
                    {"error": "Due date must be in the future."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        print("delete", pk)
        task = self.get_object(pk, request.user)
        # Check if logged-in user is the assignee
        if task.assigned_to != request.user:
            return Response(
                {"error": "You are not allowed to delete this task."},
                status=status.HTTP_403_FORBIDDEN
            )
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
