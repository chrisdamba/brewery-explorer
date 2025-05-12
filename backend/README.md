# Brewery Explorer Backend

A Django-based backend service that provides a RESTful API for exploring breweries using the Open Brewery DB API.

## Features

- RESTful API endpoints for brewery data
- Advanced filtering and search capabilities
- Data grouping and aggregation
- Error handling and logging
- Comprehensive test coverage
- Service layer pattern for API abstraction

## Tech Stack

- Python 3.8+
- Django 4.2.7
- Django REST Framework 3.14.0
- Pytest for testing
- Requests for HTTP client

## Project Structure

```
backend/
├── brewery_api/           # Main Django app
│   ├── services/          # API service layer
│   │   └── brewery_service.py
│   ├── tests/             # Test files
│   │   ├── services_test.py
│   │   └── views_test.py
│   ├── views.py           # API views
│   └── urls.py            # URL routing
├── brewery_project/       # Django project settings
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── Dockerfile           # Container configuration
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- virtualenv (recommended)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/chrisdamba/brewery-explorer.git
cd brewery-explorer/backend
```

2. Create and activate a virtual environment:

```bash
# On macOS/Linux
python -m venv env
source env/bin/activate

# On Windows
python -m venv env
env\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### List Breweries

```
GET /api/breweries/
```

Query Parameters:

- `by_type`: Filter by brewery type (micro, nano, regional, etc.)
- `by_state`: Filter by state
- `by_city`: Filter by city
- `by_name`: Filter by name
- `group_by`: Group results by attribute (brewery_type, state, city)
- `page`: Page number for pagination
- `per_page`: Number of results per page (default: 50, max: 200)

### Get Brewery by ID

```
GET /api/breweries/{id}/
```

### Search Breweries

```
GET /api/breweries/search/
```

Query Parameters:

- `query`: Search term

### Get Random Brewery

```
GET /api/breweries/random/
```

Query Parameters:

- `size`: Number of random breweries to return (default: 1)

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test brewery_api.tests.views_test

# Run with coverage
coverage run manage.py test
coverage report
```

### Test Structure

- `services_test.py`: Tests for the service layer
- `views_test.py`: Tests for API endpoints

## Service Layer

The backend implements a service layer pattern to abstract the Open Brewery DB API. This provides:

- Clear separation of concerns
- Easier testing with mock data
- Future-proofing against API changes
- Potential for caching frequently requested data

### Key Services

- `BreweryService`: Handles all interactions with the Open Brewery DB API
  - `get_breweries()`: Fetch breweries with optional filters
  - `get_brewery_by_id()`: Fetch a specific brewery
  - `search_breweries()`: Search breweries by keyword
  - `get_random_brewery()`: Get random brewery(ies)
  - `group_breweries_by_attribute()`: Group breweries by specified attribute

## Error Handling

The API implements comprehensive error handling:

- HTTP 400: Bad Request (invalid parameters)
- HTTP 404: Not Found (brewery not found)
- HTTP 500: Internal Server Error (API issues)

## Development

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Keep functions small and focused

### Adding New Features

1. Create a new branch
2. Add tests for the new feature
3. Implement the feature
4. Run tests and ensure they pass
5. Submit a pull request

## Deployment

### Docker Deployment

1. Build the Docker image:

```bash
docker build -t brewery-explorer-backend .
```

2. Run the container:

```bash
docker run -p 8000:8000 brewery-explorer-backend
```

### Production Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Configure proper database settings
3. Set up proper security measures
4. Use a production-grade server (e.g., Gunicorn)
5. Set up proper logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License
