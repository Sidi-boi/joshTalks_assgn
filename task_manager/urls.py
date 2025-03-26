from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.sign_up, name='sign_up'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/assign/', views.assign_task, name='assign_task'),
    path('tasks/<int:user_id>/', views.get_user_tasks, name='get_user_tasks'),
    path('tasks/update/<int:task_id>/', views.update_status, name='update_task_status')
]