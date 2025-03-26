from django.contrib import admin
from .models import User, Task


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'mobile')
    search_filds = ('username', 'email', 'mobile')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'created_at', 'completed_at')
    list_filter = ('status', 'created_at',)
    search_fields = ('name', 'description',)
    filter_horizontal = ('assigned_users',)
