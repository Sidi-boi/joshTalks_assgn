from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import User, Task
from .serializers import TaskSerializer, TaskCreateSerializer, TaskAssignmentSerializer


@api_view(['POST'])
def create_task(request):
    serializer = TaskCreateSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def assign_task(request):
    serializer = TaskAssignmentSerializer(data = request.data)
    
    if serializer.is_valid():
        task_id = serializer.validated_data.get('task_id')
        user_ids = serializer.validated_data.get('user_ids')

        try:
            task = Task.objects.get(pk= task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        users = User.objects.filter(pk = user_ids)

        if len(users) != len(user_ids):
            return Response({"error":"One or more users not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        task.assigned_users.set(users)

        return Response({"message":"Users assigned to the task successfully"})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_tasks(request, user_id):
    try:
            user = User.objects.get(pk = user_id)
    except User.DoesNotExist:
        return Response({"error":"User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    tasks = Task.objects.filter(assigned_users = user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)