# Task Management API

This is a Django REST Framework-based API for managing tasks and user assignments. The API supports user registration, authentication, task creation, task assignment, and status updates.

## Features
- User Registration, Login, and Logout
- Role-based access (Admin & Simple Users)
- Admins can create and assign tasks
- Users can view tasks assigned to them
- Task status updates

## Tech Stack
- Python
- Django
- Django REST Framework (DRF)
- OAuth2 Authentication

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/task-management-api.git
   cd task-management-api
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```sh
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- **Register a user:** `POST /register/`
- **Login:** `POST /login/`
- **Logout:** `POST /logout/`

### Task Management
- **Create a task (Admin only):** `POST /tasks/create/`
- **Assign a task (Admin only):** `PUT /tasks/assign/`
- **Get tasks for a user:** `GET /tasks/<user_id>/`
- **Update task status:** `PATCH /tasks/update/<task_id>/`

## Usage
Use the provided API endpoints with an HTTP client like Postman or cURL. Ensure you include the Authorization token where required.

## API Contracts

## **1. User Registration**
### **Endpoint:** `POST /register/`
### **Description:** Register a new user (admin or simple user).
### **Parameters:**
| Name     | Type   | Required | Description |
|----------|--------|----------|-------------|
| username | string | Yes      | Unique username of the user |
| email    | string | Yes      | Unique email of the user |
| mobile   | string | No       | User's mobile number |
| password | string | Yes      | User's password |
| is_admin | boolean | No      | Determines if the user is an admin (default: `false`) |

### **Sample Request (Admin User)**
```json
{
  "username": "admin_user",
  "email": "admin@example.com",
  "mobile": "1234567890",
  "password": "password123",
  "is_admin": true
}
```

### **Sample Response**
```json
{
  "message": "user created successfully"
}
```

---

## **2. User Login**
### **Endpoint:** `POST /login/`
### **Description:** Authenticates a user and starts a session.
### **Parameters:**
| Name     | Type   | Required | Description |
|----------|--------|----------|-------------|
| username | string | Yes      | User's username |
| password | string | Yes      | User's password |

### **Sample Request**
```json
{
  "username": "admin_user",
  "password": "password123"
}
```

### **Sample Response**
```json
{
  "message": "Login Successful"
}
```

---

## **3. User Logout**
### **Endpoint:** `POST /logout/`
### **Description:** Logs out an authenticated user.

### **Sample Request**
```json
{}
```

### **Sample Response**
```json
{
  "message": "Logged out successfully"
}
```

---

## **4. Create Task (Admin Only)**
### **Endpoint:** `POST /tasks/create/`
### **Description:** Creates a new task (Admins only).
### **Parameters:**
| Name       | Type   | Required | Description |
|------------|--------|----------|-------------|
| name       | string | Yes      | Task name |
| desc       | string | No       | Task description |
| task_type  | string | Yes      | Task type (`feature`, `bug`, `documentation`, `other`) |

### **Sample Request**
```json
{
  "name": "Implement Login API",
  "desc": "Create an API to authenticate users",
  "task_type": "feature"
}
```

### **Sample Response**
```json
{
  "id": 1,
  "name": "Implement Login API",
  "desc": "Create an API to authenticate users",
  "created_at": "2025-03-26T10:00:00Z",
  "task_type": "feature",
  "completed_at": null,
  "status": "pending",
  "assigned_users": []
}
```

---

## **5. Assign Task (Admin Only)**
### **Endpoint:** `PUT /tasks/assign/`
### **Description:** Assigns a task to one or more users (Only the admin who created the task can assign it).
### **Parameters:**
| Name     | Type     | Required | Description |
|----------|---------|----------|-------------|
| task_id  | integer | Yes      | ID of the task to assign |
| user_ids | array   | Yes      | List of user IDs to assign the task |

### **Sample Request**
```json
{
  "task_id": 1,
  "user_ids": [2, 3]
}
```

### **Sample Response**
```json
{
  "message": "Users assigned to the task successfully"
}
```

---

## **6. Get Tasks for a User**
### **Endpoint:** `GET /tasks/<user_id>/`
### **Description:** Retrieves all tasks assigned to a user.

### **Behavior Based on User Role:**
- If `user_id` is omitted:
  - Admin: Gets tasks created by them and tasks assigned to them.
  - Simple User: Gets tasks assigned to them.
- If `user_id` is provided:
  - Admin: Gets tasks assigned to the specified user.
  - Simple User: **Forbidden** response.

### **Sample Request (For Admin Fetching Own Tasks)**
```
GET /tasks/
```

### **Sample Response**
```json
[
  {
    "id": 1,
    "name": "Implement Login API",
    "desc": "Create an API to authenticate users",
    "created_at": "2025-03-26T10:00:00Z",
    "task_type": "feature",
    "completed_at": null,
    "status": "pending",
    "assigned_users": [{"id": 2, "username": "user1"}]
  }
]
```

### **Forbidden Response (If a simple user tries to fetch another user's tasks)**
```json
{
  "error": "You do not have permission to perform this action."
}
```

---

## **7. Update Task Status**
### **Endpoint:** `PATCH /tasks/update/<task_id>/`
### **Description:** Updates the status of a task.
- Only users assigned to the task can update it.
- Admins can update tasks they created or tasks assigned to them.

### **Parameters:**
| Name   | Type   | Required | Description |
|--------|--------|----------|-------------|
| status | string | Yes      | New task status (`pending`, `in_progress`, `completed`) |

### **Sample Request**
```json
{
  "status": "in_progress"
}
```

### **Sample Response**
```json
{
  "message": "Task status updated successfully"
}
```

### **Forbidden Response (If the user is not assigned to the task)**
```json
{
  "error": "You do not have permission to update this task."
}
```

---

## **Final Thoughts**
This API contract ensures clarity for developers consuming the API. Let me know if you need modifications! 🚀


Happy Coding! 🚀

