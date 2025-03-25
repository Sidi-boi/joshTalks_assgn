from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def __str__(self):
        return self.name
    
    # id = models.UUIDField(unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    modile = models.CharField(max_length=15, null=True, blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set", 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set", 
        blank=True
    )

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    TASK_TYPE_CHOICES = [
        ('feature', 'Feature'),
        ('bug', 'Bug'),
        ('documentation', 'Documentation'),
        ('other', 'Other'),
    ]

    def __str__(self):
        return self.name

    # id = models.UUIDField(unique=True)
    assigned_users = models.ManyToManyField(User, related_name='tasks')
    name = models.CharField(max_length=300)
    desc = models.CharField(max_length=5000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    task_type = models.CharField(max_length=100, choices=TASK_TYPE_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')



