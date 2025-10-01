# E-Commerce Backend (Django + DRF)

A modern, scalable backend service for an e-commerce platform built with Django and Django REST Framework. This project provides comprehensive user management, product catalog functionality, JWT authentication, and API documentation with a clean, modular architecture and environment-specific configurations.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/django-5.2+-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.16+-orange.svg)](https://django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15+-blue.svg)](https://postgresql.org)

---

## 🚀 Key Features

- **Modular Architecture**: Clean separation with `apps/users` and `apps/catalog`
- **JWT Authentication**: Secure token-based authentication with refresh/blacklist capabilities
- **Advanced API Features**: Filtering, sorting, pagination, and search functionality
- **Comprehensive Testing**: pytest with coverage reporting and fixtures
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation with drf-yasg
- **Environment Management**: Multi-environment configuration (development/staging/production/testing)
- **Production Ready**: Docker deployment with Nginx, Gunicorn, and PostgreSQL
- **Developer Tools**: Management commands for database seeding and development
- **Code Quality**: Configured with coverage reporting and modern Python tooling

---

## 🛠 Tech Stack

### Core Framework

- **Python 3.10+** - Modern Python with type hints support
- **Django 5.2+** - High-level web framework
- **Django REST Framework 3.16+** - Powerful toolkit for building APIs
- **PostgreSQL 15+** - Robust relational database (SQLite for development)

### Key Dependencies

- **djangorestframework-simplejwt** - JWT authentication
- **drf-yasg** - Swagger/OpenAPI documentation generation
- **django-filter** - Advanced filtering capabilities
- **python-dotenv** - Environment variable management
- **psycopg[binary]** - PostgreSQL adapter
- **gunicorn** - WSGI HTTP server for production

### Development & Testing

- **pytest** - Modern testing framework
- **pytest-django** - Django integration for pytest
- **pytest-cov** - Coverage reporting
- **uv** - Fast Python package installer and resolver

### Deployment

- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy and static file serving
- **GitHub Container Registry** - Container image hosting

---

## 📁 Project Structure

```
ecommerce_backend/
├── 📁 apps/                           # Django applications
│   ├── 📁 catalog/                    # Product catalog management
│   │   ├── models.py                  # Category & Product models
│   │   ├── serializers.py             # API serializers
│   │   ├── views.py                   # ViewSet implementations
│   │   ├── permissions.py             # Custom permissions
│   │   ├── paginations.py             # Pagination classes
│   │   ├── urls.py                    # URL routing
│   │   ├── 📁 tests/                  # Comprehensive test suite
│   │   └── 📁 management/commands/    # Management commands
│   └── 📁 users/                      # User management & authentication
│       ├── models.py                  # Custom User model
│       ├── serializers.py             # User serializers
│       ├── views.py                   # Authentication views
│       ├── urls.py                    # User-related URLs
│       ├── 📁 tests/                  # User & auth tests
│       └── 📁 management/commands/    # User seed commands
├── 📁 core/                           # Project configuration
│   ├── 📁 settings/                   # Environment-specific settings
│   │   ├── base.py                    # Shared configuration
│   │   ├── development.py             # Development overrides
│   │   ├── testing.py                 # Test environment
│   │   ├── staging.py                 # Staging environment
│   │   ├── production.py              # Production configuration
│   │   └── logging.py                 # Logging configuration
│   ├── urls.py                        # Root URL configuration
│   ├── wsgi.py                        # WSGI application
│   ├── asgi.py                        # ASGI application
│   └── 📁 templates/                  # HTML templates
├── 📁 tests/                          # Global test utilities
│   ├── constants.py                   # Test constants & fixtures
├── 📁 docs/                           # Project documentation
│   ├── ref_doc.md                     # Technical reference
│   └── wiki_doc.md                    # Development wiki
├── 📁 nginx/                          # Nginx configuration
│   ├── nginx.conf                     # Main Nginx config
│   └── proxy_params                   # Proxy parameters
├── 📁 scripts/                        # Deployment scripts
├── docker-compose.yml                  # Multi-container setup
├── Dockerfile                          # Production image
├── pyproject.toml                      # Modern Python project config
├── requirements.txt                    # Development dependencies
├── requirements-prod.txt               # Production dependencies
├── pytest.ini                         # Testing configuration
└── conftest.py                        # Root-level test fixtures
```

---

## ⚙ Environment Configuration

The project supports multiple environments through the `core/settings/` module:

- **`base.py`**: Shared configuration across all environments
- **`development.py`**: Local development with debug features
- **`testing.py`**: Optimized for fast test execution
- **`staging.py`**: Production-like environment for testing
- **`production.py`**: Hardened production configuration

Environment selection is controlled by the `ENVIRONMENT` variable in your `.env` file.

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**

   ```bash
   git clone git@github.com:joekariuki3/ecommerce_backend.git
   cd ecommerce_backend
   ```

2. **Set up environment**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Launch with Docker Compose**

   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - API: http://localhost
   - Swagger Documentation: http://localhost/swagger/
   - Admin Panel: http://localhost/admin/

### Option 2: Local Development

1. **Clone and setup virtual environment**

   ```bash
   git clone git@github.com:joekariuki3/ecommerce_backend.git
   cd ecommerce_backend
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   # Using uv (recommended - faster)
   pip install uv
   uv pip install -r requirements.txt

   # Or using pip
   pip install -r requirements.txt
   ```

3. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env with your database settings
   ```

4. **Database setup**

   ```bash
   python manage.py migrate
   python manage.py seed_users_db          # Optional: Create sample users
   python manage.py seed_category_product_db  # Optional: Create sample catalog
   ```

5. **Run development server**

   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - API: http://localhost:8000
   - Swagger Documentation: http://localhost:8000/swagger/
   - Admin Panel: http://localhost:8000/admin/

---

## 🔧 Environment Variables

Create a `.env` file based on `.env.example`:

### Required Variables

```env
# Environment
ENVIRONMENT=development  # Options: development, staging, production, testing
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost  # Use 'db' for Docker Compose
DB_PORT=5432

# Logging
ENABLE_INFO_LOGS=true
LOG_LEVEL=INFO
DJANGO_LOG_LEVEL=INFO
APPS_LOG_LEVEL=INFO
```

### Docker Production Variables

```env
ENVIRONMENT=production
DEBUG=False
POSTGRES_DB=ecommerce_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure-password
IMAGE_TAG=latest
```

---

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/swagger/ (development) or http://localhost/swagger/ (production)
- **ReDoc**: http://localhost:8000/redoc/ (development) or http://localhost/redoc/ (production)

### API Endpoints

#### Authentication & User Management

| Endpoint                   | Method           | Purpose                          | Authentication |
| -------------------------- | ---------------- | -------------------------------- | -------------- |
| `/api/users/register/`     | POST             | Create new user account          | None           |
| `/api/auth/login/`         | POST             | Obtain JWT access/refresh tokens | None           |
| `/api/auth/logout/`        | POST             | Blacklist refresh token          | Bearer Token   |
| `/api/auth/token/refresh/` | POST             | Refresh access token             | None           |
| `/api/auth/token/verify/`  | POST             | Verify token validity            | None           |
| `/api/users/`              | GET              | List users (admin only)          | Bearer Token   |
| `/api/users/{id}/`         | GET/PATCH/DELETE | User profile management          | Bearer Token   |

#### Product Catalog

| Endpoint                        | Method       | Purpose                             | Authentication |
| ------------------------------- | ------------ | ----------------------------------- | -------------- |
| `/api/catalog/categories/`      | GET          | List all categories                 | None           |
| `/api/catalog/categories/`      | POST         | Create category (admin only)        | Bearer Token   |
| `/api/catalog/categories/{id}/` | GET          | Category details                    | None           |
| `/api/catalog/categories/{id}/` | PATCH/DELETE | Update/delete category (admin only) | Bearer Token   |
| `/api/catalog/products/`        | GET          | List products with filtering/search | None           |
| `/api/catalog/products/`        | POST         | Create product (admin only)         | Bearer Token   |
| `/api/catalog/products/{id}/`   | GET          | Product details                     | None           |
| `/api/catalog/products/{id}/`   | PATCH/DELETE | Update/delete product (admin only)  | Bearer Token   |

#### Query Parameters for Product Listing

| Parameter   | Description                             | Example           |
| ----------- | --------------------------------------- | ----------------- |
| `category`  | Filter by category ID                   | `?category=1`     |
| `search`    | Search in product name/description      | `?search=laptop`  |
| `ordering`  | Sort by field (price, name, created_at) | `?ordering=price` |
| `page`      | Page number for pagination              | `?page=2`         |
| `page_size` | Items per page                          | `?page_size=20`   |

**Example API Calls:**

```bash
# Register new user
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure123", "first_name": "John", "last_name": "Doe"}'

# Login and get tokens
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure123"}'

# Search products
curl "http://localhost:8000/api/catalog/products/?search=laptop&ordering=price"

# Filter products by category
curl "http://localhost:8000/api/catalog/products/?category__id=5e7ad532-b8a8-4fe7-b02d-de3426843440"
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov=core

# Run specific test file
pytest apps/users/tests/test_user_auth.py

# Run with verbose output
pytest -v

# Run tests in parallel (faster)
pytest -n auto
```

### Test Configuration

The project uses **pytest** with comprehensive configuration in `pytest.ini`:

- **Coverage**: Automatically tracks code coverage for `apps/` and `core/`
- **Django Integration**: Full Django test database and settings support
- **Fixtures**: Shared fixtures in `conftest.py` for users, products, categories
- **Environment**: Tests run with `ENVIRONMENT=testing` setting

### Test Structure

```
├── conftest.py                    # Global fixtures and test
tests/
├── constants.py                   # Test data constants
apps/catalog/tests/
├── test_category/                 # Category model and API tests
└── test_product/                  # Product model and API tests
apps/users/tests/
├── test_user_auth.py             # Authentication flow tests
└── test_views/                   # User management tests
```

### Available Test Fixtures

- `api_client`: Unauthenticated test client
- `default_user`: Regular user instance
- `admin_user`: Admin user instance
- `authenticated_client_and_user`: Client + user tuple
- `category_factory`: Factory for creating categories
- `product_factory`: Factory for creating products

### Test Coverage

Current coverage includes:

- ✅ User registration and authentication flows
- ✅ JWT token management (login/logout/refresh)
- ✅ Product and category CRUD operations
- ✅ API permissions and authorization
- ✅ Filtering, sorting, and pagination
- ✅ Search functionality
- ✅ Error handling and validation

---

## 🗃 Data Models

### User Model (`apps.users.User`)

- Extends Django's `AbstractUser`
- Email-based authentication (no username)
- Standard fields: `first_name`, `last_name`, `email`, `is_staff`, `is_active`
- Custom manager for email-based user creation

### Category Model (`apps.catalog.Category`)

- Simple hierarchical structure for product organization
- Fields: `name`, `description`, `created_at`, `updated_at`
- Used for product filtering and navigation

### Product Model (`apps.catalog.Product`)

- Core e-commerce product entity
- Fields: `name`, `description`, `price`, `category` (ForeignKey), `created_at`, `updated_at`
- Supports filtering, searching, and sorting operations

---

## 🛠 Management Commands

### Database Seeding

```bash
# Create sample users (admin and regular users)
python manage.py seed_users_db

# Create sample categories and products
python manage.py seed_category_product_db
```

**Note**: Seeding commands are designed for development and testing environments only.

### Database Management

```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic
```

---

## 🐳 Docker Deployment

### Production Deployment

The project includes a multi-stage Docker setup optimized for production:

**Architecture**:

- **Web Container**: Django app with Gunicorn + Nginx
- **Database Container**: PostgreSQL 15
- **Image Registry**: GitHub Container Registry (`ghcr.io/joekariuki3/ecommerce_backend`)

**Deployment Steps**:

1. **Configure environment**

   ```bash
   cp .env.example .env
   # Set ENVIRONMENT=production and other production values
   ```

2. **Deploy with Docker Compose**

   ```bash
   docker compose up -d
   ```

3. **Health checks and scaling**

   ```bash
   # Check container status
   docker compose ps

   # View logs
   docker compose logs web
   docker compose logs db

   # Scale web instances
   docker compose up -d --scale web=3
   ```

### Container Images

- **Base Image**: `python:3.11-slim`
- **Web Server**: Nginx (reverse proxy) + Gunicorn (WSGI)
- **Database**: PostgreSQL 15 with health checks
- **Volumes**: Persistent PostgreSQL data storage

### Production Configuration

The production setup includes:

- ✅ Static file serving via Nginx
- ✅ Database connection pooling
- ✅ Security headers and HTTPS redirect
- ✅ Health checks for service availability
- ✅ Automated migrations on container startup
- ✅ Structured logging with JSON formatter

---

## 🚀 Upcoming Features

### Phase 2: E-commerce Core

- 🛒 **Shopping Cart**: Session and user-based cart management
- 📦 **Order Management**: Order creation, tracking, and history
- 💳 **Payment Integration**: Support for multiple payment providers
- 📊 **Inventory Management**: Stock tracking and reservations

### Phase 3: Advanced Features

- 🔍 **Enhanced Search**: PostgreSQL full-text search or Elasticsearch
- ⚡ **Caching Layer**: Redis integration for catalog and session data
- 📈 **Analytics**: Order analytics and reporting dashboards (graphQL backend)
- 🎯 **Recommendations**: Product recommendation engine

### Phase 4: Scale & Performance

- 🛡 **Rate Limiting**: API throttling and abuse prevention
- 📱 **Mobile API**: Optimized endpoints for mobile applications
- 🌐 **Internationalization**: Multi-language and currency support
- ☁ **Cloud Deployment**: AWS/Azure deployment configurations

---

## 🤝 Contributing

### Development Workflow

1. **Fork and clone**

   ```bash
   git clone git@github.com:your-username/ecommerce_backend.git
   cd ecommerce_backend
   ```

2. **Create feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Setup development environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

4. **Make changes and test**

   ```bash
   pytest --cov=apps --cov=core
   python manage.py check
   ```

5. **Commit using Conventional Commits**

   ```bash
   git commit -m "feat(catalog): add product image upload support"
   git commit -m "fix(auth): resolve token refresh issue"
   git commit -m "docs(api): update authentication examples"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Create PR targeting 'develop' branch
   ```

### Code Quality Standards

- **Testing**: Maintain >90% test coverage
- **Documentation**: Update API docs for new endpoints
- **Type Hints**: Use Python type annotations
- **Security**: Follow Django security best practices
- **Performance**: Consider database query optimization

---

## 📖 Additional Documentation

For detailed technical information, see:

- **`docs/ref_doc.md`**: Complete technical reference and requirements
- **`docs/wiki_doc.md`**: Development wiki and architecture decisions
- **API Documentation**: Available at `/swagger/` and `/redoc/` endpoints

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Support

- **Issues**: [GitHub Issues](https://github.com/joekariuki3/ecommerce_backend/issues)
- **Email**: joelkmuhoho@gmail.com

---

_Built with ❤️ using Django and Django REST Framework_
