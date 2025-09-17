```markdown
# ALX Travel App

A comprehensive Django REST API for a travel listing platform, featuring property listings, reviews, and booking management.

## Features

- **Property Listings**: Create, view, update, and delete travel property listings
- **User Reviews**: Rate and review properties
- **Booking System**: Manage bookings with different statuses
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Search & Filter**: Advanced filtering and search capabilities
- **Admin Interface**: Django admin for easy management

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: MySQL
- **Documentation**: Swagger (drf-yasg)
- **Task Queue**: Celery with Redis
- **CORS**: django-cors-headers

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/alx_travel_app.git
   cd alx_travel_app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- **Listings**: `/api/listings/`
- **Listing Detail**: `/api/listings/{id}/`
- **Reviews**: `/api/listings/{listing_id}/reviews/`
- **Bookings**: `/api/bookings/`
- **API Documentation**: `/swagger/`

## Project Structure

```
alx_travel_app/
├── manage.py
├── requirements.txt
├── alx_travel_app/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── listings/
    ├── models.py
    ├── views.py
    ├── serializers.py
    └── ...
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.