# BookStore Project

## Overview

BookStore is a Django application that allows users to register, log in, and manage a collection of books. Each book is associated with an author, and users can perform CRUD operations on their books. The application also includes APIs for user authentication and book management.

## Features

- User Registration
- User Login
- CRUD operations for books
- List books by author
- Token-based authentication
- Middleware for logging requests

## Technologies Used

- Django
- Django REST Framework
- PostgreSQL

## Setup and Installation

### Prerequisites

- Python
- PostgreSQL
- pip (Python package installer)

### Installation Steps

1. **Clone the repository:**

    ```bash
    git clone <repo link>
    cd bookstore
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database:**

    Update the `DATABASES` setting in `bookstore/settings.py` with your PostgreSQL credentials.

5. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Authentication

- **Register:** `/accounts/register/` (POST)
    - Request: `{ "username": "user", "password": "pass", "email": "user@example.com" }`
    - Response: `{ "message": "User created successfully" }`

- **Login:** `/accounts/login/` (POST)
    - Request: `{ "username": "user", "password": "pass" }`
    - Response: `{ "token": "your-auth-token" }`
 
- **Logout:** `/accounts/logout/` (POST)
    - Response: `{ "message": "Logout successful" }`

### Books

- **List Books:** `/api/books/` (GET)
    - Returns a list of books for the authenticated user.

- **Create Book:** `/api/books/` (POST)
    - Request: `{ "title": "Book Title", "author": { "name": "Author Name" }, "published_date": "2023-01-01" }`
    - Response: Details of the created book.

- **Create Book with existing Athor:** `/api/books/` (POST)
    - Request: `{ "title": "Book Title", "author": { "id": "1" }, "published_date": "2023-01-01" }`
    - Response: Details of the created book.

- **Retrieve Book:** `/api/books/{id}/` (GET)
    - Returns details of the specified book.

- **Update Book:** `/api/books/{id}/` (PUT)
    - Request: `{ "title": "New Title", "author": { "id": 1 }, "published_date": "2023-01-01" }`
    - Response: Details of the updated book.

- **Delete Book:** `/api/books/{id}/` (DELETE)
    - Response: `{ "message": "Book deleted successfully" }`

- **List Books by Author:** `/api/books/by-author/{author_id}/` (GET)
    - Returns a list of books by the specified author for the authenticated user.

## Middleware

### LogRequestMiddleware

This middleware logs the HTTP method and path of incoming requests.

## Running Tests

To run the tests, use the following command:

```bash
python manage.py test
