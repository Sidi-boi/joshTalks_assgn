from rest_framework import serializers
from .models import User, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'mobile')  


class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True) 
    class Meta:
        model = Task
        fields = ('id', 'name', 'desc', 'created_at', 'task_type', 'completed_at', 'status', 'assigned_users')

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
         model = Task
         fields = ['name', 'description', 'task_type']


class TaskAssignmentSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    user_ids = serializers.ListField(child=serializers.IntegerField())