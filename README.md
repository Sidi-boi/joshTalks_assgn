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

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Create a Pull Request

## License
This project is licensed under the MIT License.

---
Happy Coding! 🚀

