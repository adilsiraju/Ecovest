# Development Setup Guide

This guide will help you set up a local development environment for Ecovest.

## 🛠️ Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.11+** - [Download Python](https://python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **PostgreSQL** (optional, for production-like setup) - [Download PostgreSQL](https://postgresql.org/download/)
- **Redis** (optional, for caching) - [Download Redis](https://redis.io/download)

## 🚀 Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/adilsiraju/Ecovest.git
cd Ecovest
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# For development, default values should work
```

### 5. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 6. Start Development Server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the application running!

## 🏗️ Project Structure

```
Ecovest/
├── 📁 core/                    # Core application
│   ├── models.py              # Core models
│   ├── views.py               # Core views
│   ├── urls.py                # URL routing
│   └── templates/             # Core templates
├── 📁 initiatives/            # Sustainable projects
│   ├── models.py              # Initiative models
│   ├── views.py               # Initiative views
│   ├── forms.py               # Django forms
│   └── templates/             # Initiative templates
├── 📁 investments/            # Investment management
│   ├── models.py              # Investment models
│   ├── impact_calculator.py   # AI prediction engine
│   ├── portfolio_analyzer.py  # Portfolio analytics
│   └── models/                # ML model files
├── 📁 users/                  # User management
│   ├── models.py              # User profile models
│   ├── forms.py               # User forms
│   └── signals.py             # User signals
├── 📁 onboarding/             # User onboarding
├── 📁 static/                 # Static assets
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript files
│   └── images/                # Images
├── 📁 media/                  # User uploads
├── 📁 templates/              # Global templates
├── manage.py                  # Django management
├── requirements.txt           # Python dependencies
└── .env.example              # Environment template
```

## 🔧 Development Tools

### Code Quality Tools

Install development dependencies:
```bash
pip install black flake8 isort mypy pytest-django
```

#### Code Formatting
```bash
# Format code with Black
black .

# Sort imports
isort .
```

#### Linting
```bash
# Check code style
flake8 .

# Type checking
mypy .
```

#### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test initiatives

# Run with coverage
pip install coverage
coverage run manage.py test
coverage report
coverage html  # Generate HTML report
```

### Pre-commit Hooks

Set up pre-commit hooks to ensure code quality:

```bash
pip install pre-commit
pre-commit install
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

## 🗄️ Database Management

### Using SQLite (Default)
SQLite is used by default for development. No additional setup required.

### Using PostgreSQL (Recommended for Production-like Setup)

1. **Install PostgreSQL**
2. **Create database and user**:
   ```sql
   CREATE DATABASE ecovest_dev;
   CREATE USER ecovest_user WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE ecovest_dev TO ecovest_user;
   ```

3. **Update .env file**:
   ```env
   DATABASE_URL=postgresql://ecovest_user:password@localhost:5432/ecovest_dev
   ```

4. **Install PostgreSQL adapter**:
   ```bash
   pip install psycopg2-binary
   ```

### Database Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development only)
python manage.py flush

# Create superuser
python manage.py createsuperuser

# Load fixture data
python manage.py loaddata fixtures/sample_data.json

# Dump data to fixture
python manage.py dumpdata --indent 2 > fixtures/sample_data.json
```

## 🤖 AI Model Development

### Setting up ML Environment

```bash
# Install Jupyter for model development
pip install jupyter notebook

# Start Jupyter
jupyter notebook
```

### Working with Impact Prediction Models

1. **Generate models**:
   ```bash
   python investments/generate_models.py
   ```

2. **Test models**:
   ```bash
   jupyter notebook investments/model_testing.ipynb
   ```

3. **Using the calculator**:
   ```python
   from investments.impact_calculator import ImpactCalculator
   
   calculator = ImpactCalculator()
   impact = calculator.predict_impact(
       investment_amount=100000,
       category_names=['Renewable Energy'],
       project_duration_months=12,
       project_scale=3,
       location='Karnataka',
       technology_type='Solar'
   )
   ```

## 🎨 Frontend Development

### Static Files

```bash
# Collect static files
python manage.py collectstatic

# During development, static files are served automatically
```

### CSS/JavaScript

- CSS files are in `static/css/`
- JavaScript files are in `static/js/`
- Images are in `static/images/`

### Templates

- Base templates are in `templates/`
- App-specific templates are in `<app>/templates/<app>/`

## 🧪 Testing

### Test Structure

```
tests/
├── test_models.py      # Model tests
├── test_views.py       # View tests
├── test_forms.py       # Form tests
└── test_utils.py       # Utility tests
```

### Writing Tests

```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from initiatives.models import Initiative, Category

User = get_user_model()

class InitiativeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Renewable Energy'
        )
    
    def test_initiative_creation(self):
        initiative = Initiative.objects.create(
            title='Test Solar Project',
            description='A test solar project',
            category=self.category,
            creator=self.user,
            target_amount=1000000
        )
        self.assertEqual(initiative.title, 'Test Solar Project')
        self.assertEqual(initiative.category, self.category)
```

### Test Commands

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test initiatives.tests.test_models

# Run specific test class
python manage.py test initiatives.tests.test_models.InitiativeModelTest

# Run with verbose output
python manage.py test --verbosity=2

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🔍 Debugging

### Django Debug Toolbar

Install Django Debug Toolbar for debugging:

```bash
pip install django-debug-toolbar
```

Add to `INSTALLED_APPS` in development settings:
```python
INSTALLED_APPS = [
    # ... other apps
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ... other middleware
]

INTERNAL_IPS = [
    '127.0.0.1',
]
```

### Logging

Configure logging for development:

```python
# settings/development.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

## 📱 Mobile Development

### Responsive Design

The platform uses Bootstrap 5 for responsive design. Test on different screen sizes:

```bash
# Use browser dev tools or
# Test with different viewport sizes
```

## 🔒 Security in Development

### Security Settings

For development, certain security features are disabled:

```python
# settings/development.py
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

### Environment Variables

Never commit sensitive data:
- Add `.env` to `.gitignore`
- Use `.env.example` for documentation
- Use different values for development/production

## 🚀 Hot Reloading

Django automatically reloads when you change Python files. For frontend changes:

```bash
# Watch for CSS/JS changes (if using build tools)
npm run watch  # If using Node.js build tools
```

## 📊 Performance Monitoring

### Django Extensions

Install django-extensions for additional management commands:

```bash
pip install django-extensions
```

Useful commands:
```bash
# Show URL patterns
python manage.py show_urls

# Generate model graph
python manage.py graph_models -a -o models.png

# Run development server with enhanced features
python manage.py runserver_plus
```

## 🔧 IDE Setup

### VS Code

Recommended extensions:
- Python
- Django
- GitLens
- Prettier
- Black Formatter

### PyCharm

Configure Django support:
1. Go to Settings → Languages & Frameworks → Django
2. Enable Django support
3. Set Django project root
4. Set settings file path

## 🆘 Troubleshooting

### Common Issues

1. **Import errors**:
   ```bash
   # Ensure virtual environment is activated
   # Check PYTHONPATH
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Database migration issues**:
   ```bash
   # Reset migrations (development only)
   rm */migrations/0*.py
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Static files not loading**:
   ```bash
   python manage.py collectstatic
   # Check STATIC_URL and STATICFILES_DIRS
   ```

4. **Port already in use**:
   ```bash
   # Use different port
   python manage.py runserver 8001
   
   # Or kill process using port 8000
   # Windows: netstat -ano | findstr :8000
   # macOS/Linux: lsof -ti:8000 | xargs kill
   ```

### Getting Help

- Check the [documentation](README.md)
- Search [existing issues](https://github.com/adilsiraju/Ecovest/issues)
- Ask questions in [discussions](https://github.com/adilsiraju/Ecovest/discussions)
- Contact the development team

Happy coding! 🚀
