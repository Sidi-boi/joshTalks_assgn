from rest_framework import serializers
from .models import User, Task
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'mobile', 'is_admin')  
        read_only_fields = ['id', 'username']


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = User
        fields = ('id','username', 'email', 'mobile', 'password')
        

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            mobile = validated_data.get('mobile',None),
            is_admin = validated_data.get('is_admin', False)
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True) 
    class Meta:
        model = Task
        fields = ('id', 'name', 'desc', 'created_at', 'task_type', 'completed_at', 'status', 'assigned_users')

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
         model = Task
         fields = ['name', 'desc', 'task_type', 'created_by']
         read_only_fields = ['created_by']


class TaskAssignmentSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    user_ids = serializers.ListField(child=serializers.IntegerField())