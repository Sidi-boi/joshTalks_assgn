from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, authenticate

from .models import User, Task
from .serializers import TaskSerializer, TaskCreateSerializer, TaskAssignmentSerializer, UserCreateSerializer, UserLoginSerializer 


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(reqeust):
    serializer = UserCreateSerializer(data = reqeust.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message":"user created successfully"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        
        

        if not User.objects.filter(username = username).exists():
            return Response({'error':"Invalid Username"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error':"Incorrect Password, Please try again"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            login(request, user)
            return Response({'message':'Login Successful'},status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        logout(request)
        return Response({'message': 'Logged out successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def is_admin_user(user):
    return user.is_authenticated and user.is_admin

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    if not is_admin_user(request.user):
        return Response({"error":"Only Admins can create a task"}, status=status.HTTP_401_UNAUTHORIZED)
    
    data = request.data.copy()
    data['created_by'] = request.user.id

    serializer = TaskCreateSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def assign_task(request):

    if not is_admin_user(request.user):
        return Response({"error":"Only Admin can assign tasks"}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = TaskAssignmentSerializer(data = request.data)
    

    if serializer.is_valid():
        task_id = serializer.validated_data.get('task_id')
        user_ids = serializer.validated_data.get('user_ids')

        try:
            task = Task.objects.get(pk= task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        if task.created_by != request.user:
            return Response({"error": "Only the admin who created the task can assign it."}, status=status.HTTP_403_FORBIDDEN)
        
        users = User.objects.filter(pk = user_ids)
        if len(users) != len(user_ids):
            return Response({"error":"One or more users not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        task.assigned_users.set(users)
        return Response({"message":"Users assigned to the task successfully"})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_tasks(request, user_id=None):
    if user_id:  # Case 3: If user_id is provided
        try:
            target_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if is_admin_user(request.user):
            tasks = Task.objects.filter(assigned_users=target_user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Forbidden: Only admins can view other users' tasks."}, status=status.HTTP_403_FORBIDDEN)

    else:  # Case 1 and Case 2: No user_id provided and user or admin
        if is_admin_user(request.user):
            created_tasks = Task.objects.filter(created_by=request.user)
            assigned_tasks = Task.objects.filter(assigned_users=request.user)
            tasks = created_tasks.union(assigned_tasks) 
        else:
            tasks = Task.objects.filter(assigned_users=request.user)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_status(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user has permission to update the task
    if not (is_admin_user(request.user) and (task.created_by == request.user)) and request.user not in task.assigned_users.all():
        return Response({"error": "Forbidden: You can only update tasks assigned to you or tasks you created (if admin)."},
                        status=status.HTTP_403_FORBIDDEN)

    # Allow updating only the status field
    status_choices = [choice[0] for choice in Task.STATUS_CHOICES]
    new_status = request.data.get('status')

    if new_status not in status_choices:
        return Response({"error": "Invalid status. Choose from: " + ", ".join(status_choices)},
                        status=status.HTTP_400_BAD_REQUEST)

    task.status = new_status
    task.save()

    return Response({"message": "Task status updated successfully", "task_id": task.id, "new_status": task.status},
                    status=status.HTTP_200_OK)

