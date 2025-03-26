from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Task

class TaskManagementAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create an admin user
        self.admin_user = User.objects.create_user(
            username="adminuser", email="admin@example.com", password="adminpass", is_admin=True
        )
        
        # Create a normal user
        self.user = User.objects.create_user(
            username="testuser", email="user@example.com", password="testpass"
        )
        
        # Obtain authentication tokens
        self.client.login(username="adminuser", password="adminpass")
        
        # Create a task by admin
        self.task = Task.objects.create(
            name="Test Task",
            desc="Task description",
            task_type="feature",
            status="pending"
        )
        self.task.assigned_users.add(self.user)
        self.admin_user.set_password("adminpass")
        self.admin_user.save()

        print(User.objects.all())  # Check if users exist in test DB

    def test_user_registration(self):
        data = {"username": "newuser", "email": "newuser@example.com", "password": "newpass"}
        response = self.client.post("/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        data = {"username": "adminuser", "password": "adminpass"}
        response = self.client.post("/login/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_create_task_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"name": "New Task", "desc": "New Task Desc", "task_type": "feature"}
        response = self.client.post("/tasks/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_assign_task_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"task_id": self.task.id, "user_ids": [self.user.id]}
        response = self.client.put("/tasks/assign/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user, self.task.assigned_users.all())

    def test_get_user_tasks(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/tasks/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task_status(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"status": "completed"}
        response = self.client.patch(f"/tasks/update/{self.task.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "completed")

    def test_logout(self):
        response = self.client.post("/logout/")  # Call logout API
        self.assertEqual(response.status_code, 200)
 