# TransROM-IA Backend

A robust FastAPI-based backend service for the TransROM-IA project, featuring async database operations, OAuth authentication, and comprehensive API documentation.

## 🚀 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) 0.115.12
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/) 0.34.0
- **Database**: PostgreSQL with [SQLAlchemy](https://www.sqlalchemy.org/) 2.0.40
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) 1.13.1
- **Authentication**: JWT with [python-jose](https://python-jose.readthedocs.io/)
- **Data Validation**: [Pydantic](https://docs.pydantic.dev/) 2.11.0
- **OAuth Integration**: Google OAuth2 with google-auth

## 📦 Current Project Structure and Modules

### Application Structure
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py   # Authentication endpoints
│   │       │   └── users.py  # User management
│   │       └── api.py        # API router configuration
│   ├── core/
│   │   ├── config.py        # Settings and configuration
│   │   ├── exceptions.py    # Exception handlers
│   │   └── logging.py       # Logging configuration
│   ├── database/
│   │   └── session.py       # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── main.py             # Application entry point
├── scripts/
│   └── init_db.py          # Database initialization
├── tests/                  # Test suite
└── alembic/                # Database migrations
```

### Main Application Components

#### 1. Entry Point (main.py)
```python
def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Application initialization
    # Middleware configuration
    # Router inclusion
    # Exception handling setup
```

#### 2. Database Management
- `alembic/` - Database migration management
- `init_db.py` - Initial database setup script
- `database/session.py` - Database connection handling

#### 3. API Layer Organization
```mermaid
graph TD
    A[main.py] --> B[api_router]
    B --> C[endpoints]
    C --> D[auth.py]
    C --> E[users.py]
    D --> F[services]
    E --> F
```

#### 4. Core Functionality
- `core/config.py` - Environment and app configuration
- `core/exceptions.py` - Custom exception handlers
- `core/logging.py` - Logging setup

### Development Tools

#### Available Commands
```bash
# Server
uvicorn app.main:app --reload

# Database
alembic upgrade head
python scripts/init_db.py

# Testing
pytest
pytest --cov=app tests/

# Linting
ruff check .
black .
isort .
```

#### Code Quality Tools
```yaml
# From .pre-commit-config.yaml
- ruff
- black
- isort
- mypy
- pytest
```

### Environment Configuration
```env
# Required Environment Variables
DATABASE_URL=postgresql://user:password@localhost:5432/transrom
SECRET_KEY=your-secret-key
ENVIRONMENT=development
API_V1_STR=/api/v1
PROJECT_NAME=TransROM-IA
```

### Testing Structure
```
tests/
├── conftest.py           # Test fixtures
├── test_api/            # API endpoint tests
└── test_models/         # Database model tests
```

## 🛠️ Setup and Installation

1. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   - Copy `.env.example` to `.env`
   - Update environment variables:
     ```env
     DATABASE_URL=postgresql://user:password@localhost:5432/transrom
     SECRET_KEY=your-secret-key
     GOOGLE_CLIENT_ID=your-google-client-id
     GOOGLE_CLIENT_SECRET=your-google-client-secret
     ```

4. **Database Setup**
   ```bash
   alembic upgrade head
   ```

5. **Run Development Server**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`

## 📚 API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## 📜 Available Scripts

- `alembic revision --autogenerate -m "message"` - Generate migration
- `alembic upgrade head` - Apply migrations
- `pytest` - Run tests
- `ruff check .` - Run linter
- `black .` - Format code
- `isort .` - Sort imports

## 🔒 Authentication

The API supports multiple authentication methods:
- JWT Token Authentication
- Google OAuth2
- API Key Authentication (for service-to-service communication)

## 🔗 Dependencies

### Core Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pydantic` - Data validation
- `alembic` - Database migrations
- `psycopg2-binary` - PostgreSQL adapter

### Authentication & Security
- `python-jose[cryptography]` - JWT handling
- `passlib[bcrypt]` - Password hashing
- `python-multipart` - Form data parsing
- `google-auth` - Google OAuth integration

### Development Dependencies
- `ruff` - Linting
- `pytest` - Testing
- `black` - Code formatting
- `isort` - Import sorting
- `pre-commit` - Git hooks

## 🤝 Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the terms of the [LICENSE](../LICENSE) file.

## 📦 Modules and Interactions

### API Structure
```
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── auth.py     # Authentication endpoints
│       │   └── users.py    # User management endpoints
│       └── api.py          # API router configuration
├── core/
│   ├── config.py           # Application configuration
│   ├── security.py         # Security utilitiesao 
│   └── deps.py            # Dependency injection
├── models/
│   ├── user.py            # User database model
│   └── base.py            # Base model configuration
└── schemas/
    ├── user.py            # User Pydantic schemas
    └── token.py           # Authentication schemas
```

### Key Modules and Their Interactions

#### 1. Authentication System
```mermaid
graph TD
    A[auth.py] --> B[security.py]
    B --> C[user.py Model]
    A --> D[token.py Schema]
    E[Google OAuth] --> A
    F[JWT] --> B
```

#### 2. Database Operations
- `database/session.py` - Database session management
- `database/base.py` - Base database configuration
- `models/*.py` - SQLAlchemy models
- `alembic/versions/*` - Database migrations

#### 3. Core Services
- `services/auth.py` - Authentication business logic
- `services/user.py` - User management operations
- `services/email.py` - Email service integration
- `services/storage.py` - File storage operations

#### 4. Scripts and Utilities
```
scripts/
├── db/
│   ├── init_db.py        # Database initialization
│   └── seed_data.py      # Test data seeding
├── backup/
│   └── backup_db.py      # Database backup utility
└── maintenance/
    └── cleanup_logs.py   # Log maintenance
```

#### 5. API Endpoints Flow
1. Request → FastAPI Router
2. Middleware (Authentication, Logging)
3. Dependency Injection (from core/deps.py)
4. Endpoint Handler
5. Service Layer
6. Database Operation
7. Response Serialization

#### 6. Testing Structure
```
tests/
├── conftest.py           # Test configuration
├── test_api/            # API endpoint tests
├── test_services/       # Service layer tests
└── test_models/        # Database model tests
```

#### 7. Configuration Management
- `core/config.py` - Environment configuration
- `alembic.ini` - Database migration settings
- `.env` - Environment variables
- `pyproject.toml` - Project dependencies and tools

#### 8. Logging System
```
logs/
├── app.log              # Application logs
├── error.log           # Error logs
└── access.log         # API access logs
``` 