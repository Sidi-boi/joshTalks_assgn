from django.urls import path
from . import views

urlpatterns = [
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/assign/', views.assign_task, name='assign_task'),
    path('users/<int:user_id>/tasks/', views.get_user_tasks, name='get_user_tasks')
]