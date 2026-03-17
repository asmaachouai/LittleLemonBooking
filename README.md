# 🍋 Little Lemon — Table Reservation API

A full-stack Django REST API powering the table reservation system for the **Little Lemon** restaurant. Built as the capstone project for the Meta Back-End Developer specialization.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Database Setup](#database-setup)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Testing](#testing)
- [Deployment Checklist](#deployment-checklist)
- [Contributing](#contributing)

---

## Overview

Little Lemon is a restaurant web application that allows customers to browse the food menu and reserve a table online. The backend exposes a RESTful API built with **Django REST Framework (DRF)**, connected to a **MySQL** database, and protected by **token-based authentication**.

**Core Features:**
- Browse the food menu (GET)
- Create, update, and delete menu items (CRUD)
- Create and manage table bookings
- User registration, login, and logout
- Token-based authentication — only logged-in users can book a table
- Unit-tested API endpoints

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Framework | Django 4.x |
| API Layer | Django REST Framework (DRF) |
| Database | MySQL |
| Authentication | DRF Token Authentication |
| Version Control | Git + GitHub |
| HTTP Testing | Insomnia / Postman / HTTPie |
| IDE | VS Code |

---

## Project Structure

```
littlelemon/
├── littlelemon/          # Project package
│   ├── settings.py       # Project settings (DB, auth, installed apps)
│   ├── urls.py           # Root URL dispatcher
│   └── wsgi.py
├── restaurant/           # Main application
│   ├── models.py         # Menu and Booking models
│   ├── serializers.py    # DRF serializers (JSON conversion)
│   ├── views.py          # API views (class-based)
│   ├── urls.py           # App-level URL configuration
│   └── tests/
│       └── test_models.py
├── static/               # Static assets (CSS, JS, images)
├── manage.py
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL Server running locally
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/littlelemon.git
cd littlelemon
```

### 2. Create and Activate a Virtual Environment

```bash
# Create virtual environment
python -m venv littlelemon-env

# Activate — macOS/Linux
source littlelemon-env/bin/activate

# Activate — Windows
littlelemon-env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` includes:

```
django
djangorestframework
mysqlclient
```

### 4. Configure Environment Variables

Create a `.env` file at the project root (never commit this):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=littlelemon
DB_USER=your-mysql-user
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000/restaurant/` in your browser.

---

## Database Setup

The project uses **MySQL**. Configure the database connection in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'littlelemon',
        'USER': 'your-mysql-user',
        'PASSWORD': 'your-mysql-password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Models

**Menu**

| Field | Type | Description |
|---|---|---|
| `id` | AutoField | Primary key |
| `title` | CharField | Name of the menu item |
| `price` | DecimalField | Price of the item |
| `inventory` | IntegerField | Stock count |

**Booking**

| Field | Type | Description |
|---|---|---|
| `id` | AutoField | Primary key |
| `name` | CharField | Guest name |
| `no_of_guests` | IntegerField | Number of guests |
| `booking_date` | DateTimeField | Reservation date and time |

---

## API Endpoints

The base URL is `http://localhost:8000/`.

### Menu Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/restaurant/menu/` | List all menu items | No |
| POST | `/restaurant/menu/` | Add a new menu item | Yes |
| GET | `/restaurant/menu/<id>/` | Get a single menu item | No |
| PUT | `/restaurant/menu/<id>/` | Update a menu item | Yes |
| DELETE | `/restaurant/menu/<id>/` | Delete a menu item | Yes |

### Booking Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/restaurant/booking/` | List all bookings | Yes |
| POST | `/restaurant/booking/` | Create a new booking | Yes |
| GET | `/restaurant/booking/<id>/` | Get a single booking | Yes |
| PUT | `/restaurant/booking/<id>/` | Update a booking | Yes |
| DELETE | `/restaurant/booking/<id>/` | Cancel a booking | Yes |

### Auth Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/token/login/` | Obtain an auth token |
| POST | `/auth/token/logout/` | Invalidate the token |
| POST | `/auth/users/` | Register a new user |

---

## Authentication

This project uses **DRF Token Authentication**.

### Setup (already in `settings.py`)

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'restaurant',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

### Obtain a Token

Send a `POST` request to `/auth/token/login/`:

```json
{
  "username": "your-username",
  "password": "your-password"
}
```

**Response:**

```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Use the Token

Include it in the `Authorization` header for all protected requests:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## Testing

Tests are located in `restaurant/tests/`.

### Run All Tests

```bash
python manage.py test
```

### What is Tested

- **Model tests** — validate that `Menu` and `Booking` model instances are created correctly
- **API tests** — validate GET/POST responses, status codes, and JSON structure using DRF's test client
- **Auth tests** — verify that unauthenticated requests to protected routes return `HTTP 401`

### Example Test

```python
from django.test import TestCase
from restaurant.models import Menu

class MenuModelTest(TestCase):
    def test_create_menu_item(self):
        item = Menu.objects.create(title="Greek Salad", price=9.99, inventory=50)
        self.assertEqual(str(item.title), "Greek Salad")
        self.assertEqual(item.price, 9.99)
```

You can also use the **DRF browsable API** by visiting `http://localhost:8000/restaurant/menu/` in your browser, or use **Insomnia / Postman** to fire HTTP requests manually.

---

## Deployment Checklist

Before deploying to production, make sure to:

- [ ] Set `DEBUG = False` in `settings.py`
- [ ] Set a strong, unique `SECRET_KEY` via environment variables
- [ ] Add your domain to `ALLOWED_HOSTS`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Switch to a production-grade web server (e.g., Gunicorn + Nginx)
- [ ] Use environment variables for all secrets (never hardcode credentials)
- [ ] Enable HTTPS

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## License

This project was built as part of the **Meta Back-End Developer Professional Certificate** capstone. It is intended for educational purposes.

---

> Built with 🍋 and Django by a back-end developer in training.
