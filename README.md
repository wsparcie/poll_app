# Django Poll App

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-success.svg)](https://www.djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-4.0-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Alpha-yellow.svg)]()
[![Last Updated](https://img.shields.io/badge/Last%20Updated-May%202025-brightgreen.svg)](https://github.com/yourusername/poll_app)

A simple Django-based polling application that enables secure creation and management of polls with token-based voting system. Features real-time results tracking, responsive UI, and robust authentication.

## Features in Detail

### Core Functionality
- **Poll Management**:
  - Create and manage multiple polls
  - Add/remove choices dynamically
  - Set poll activation/deactivation
  - Real-time vote tracking
  - Results visualization

### Data Management
- **Admin Interface**:
  - Comprehensive poll management
  - User management
  - Token management
  - Vote tracking
  - Statistics and reporting

### Security Features
- **Authentication System**:
  - User registration and login
  - Password validation and security
  - Session management
  
- **Token System**:
  - Unique voting tokens for each poll
  - Prevent duplicate voting
  - Token validation and expiry
  - Secure token generation

### User Interface
- **Responsive Design**:
  - Bootstrap 4.0 framework
  - Mobile-first approach
  - Dark theme
  - Interactive elements
  - AJAX-powered updates

## Prerequisites

- Python 3.13+
- Django 5.0+
- Web browser (Chrome, Firefox, Safari)
- Required Python packages:

  ```
  django
  python-decouple
  django-crispy-forms
  ```

## Installation and configuration

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

3. Set up database:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Run development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Login or register a new account
2. Create a new poll with multiple choice options
3. Share the poll using generated tokens
4. Track votes and view results in real-time
5. Manage polls through the admin interface

## License

MIT License - feel free to use and modify as needed.
