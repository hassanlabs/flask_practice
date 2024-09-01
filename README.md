# Flask Login and Registration API

A simple Flask application for user registration and login, utilizing SQLAlchemy for database management and Werkzeug for password hashing.

## Features

- User registration
- User login
- SQLite database

## Requirements

- Python 3.6 or higher
- Flask
- Flask-SQLAlchemy
- Werkzeug

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Hassantariq080/flask_practice.git
   cd flask_practice
2. Create and activate a virtual environment:
   python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
3. Install required packages:
   pip install -r requirements.txt
4. Set the environment variable for Flask:
   export FLASK_APP=run.py  # Use `set FLASK_APP=run.py` on Windows
Usage:
1. flask run
2. Register a new user (POST to /register):
   {
  "first_name": "Hassan",
  "last_name": "Tariq",
  "username": "hassantariq",
  "email": "hassantariq@example.com",
  "password": "HassanSecurePass123!",
  "confirm_password": "HassanSecurePass123!",
  "phone_number": "555-5678",
  "age": 30
  }
3. Login (POST to /login):
   {
  "username": "hassantariq",
  "password": "HassanSecurePass123!"
  }

License
MIT License.

Author
Hassan Tariq

