# AIcademy

A modern, scalable FastAPI application following Clean Architecture principles with JWT authentication, database migrations, and comprehensive API documentation.

## 🏗️ Architecture

This project follows Clean Architecture principles:

```
app/
├── domain/              # Business logic and interfaces
│   ├── adapters/        # Port interfaces (hashing, JWT)
│   ├── models/          # Domain models
│   └── repositories/    # Repository interfaces
├── infrastructure/      # External concerns
│   ├── configs/         # Configuration management
│   ├── controllers/     # HTTP controllers and DTOs
│   ├── entities/        # Database entities
│   ├── repositories/    # Repository implementations
│   ├── services/        # External service implementations
│   ├── dependencies/    # Dependency injection
│   ├── common/         # Shared infrastructure
│   │   ├── exceptions/  # Custom exception classes
│   │   ├── middlewares/ # HTTP middlewares
│   │   └── dtos/        # Data transfer objects
└── usecases/           # Application business logic
    ├── auth/           # Authentication use cases
    └── user/           # User management use cases
```

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.116.1
- **Database**: MySQL 8.0 with SQLAlchemy ORM
- **Migrations**: Alembic
- **Password Hashing**: bcrypt
- **Containerization**: Docker & Docker Compose
- **Code Quality**: Black (formatting), Flake8 (linting)

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- MySQL 8.0 (or use Docker container)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/tuyenlt/AIcademy.git
cd AIcademy
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# Application Configuration
APP_NAME=AIcademy
APP_URL=http://localhost:8000
API_KEY=your-secret-api-key

# JWT Configuration
JWT_ACCESS_SECRET=your-super-secret-access-key
JWT_REFRESH_SECRET=your-super-secret-refresh-key
JWT_ACCESS_EXPIRES_SECONDS=3600
JWT_REFRESH_EXPIRES_SECONDS=604800

# Database Configuration
DATABASE_NAME=aicademy_db
DATABASE_USER=admin
DATABASE_PASSWORD=your-secure-password
DATABASE_HOST=db
DATABASE_PORT=3306
DATABASE_SCHEMA=aicademy_db

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
CORS_CREDENTIALS=true
CORS_METHODS=["GET", "POST", "PUT", "DELETE"]
CORS_HEADERS=["*"]
```

### 3. Run with Docker (Recommended)

```bash
# Build and start all services
docker-compose up

# Stop services
docker-compose down
```

### 4. Run Locally (Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: **endpoint/docs
- **ReDoc**: **endpoint/redoc
- **OpenAPI JSON**: **endpoint/openapi.json

## 📁 Project Structure Details

### Core Components

- **Controllers**: Handle HTTP requests and responses
- **Use Cases**: Contain business logic and orchestrate domain operations
- **Repositories**: Data access layer with interface/implementation separation
- **Services**: External service integrations (JWT, hashing)
- **Middlewares**: Request/response processing (authentication, logging)
- **DTOs**: Data transfer objects for API contracts

## 🔧 Development Commands

### Using Makefile Commands

```bash
# Format code
make format

# Lint code  
make lint

# Start development server
make run

# Generate migration (with auto timestamp)
make migration_gen

# Apply migrations
make migration_run

# Rollback last migration
make migration_revert

# Show current migration status
make migration_current

# Show migration history
make migration_history

# Run database seeds
make seed
```

### Direct Commands (if needed)

```bash
# Exec into the docker container 
docker exec -it aicademy_app bash

# Docker development
docker-compose up --build

# Manual migration with custom message
alembic revision --autogenerate -m "Your custom message"
```

## 🐳 Docker Configuration

### Services

- **app**: FastAPI application container
- **db**: MySQL 8.0 database container

### Volumes

- Database data persistence
- Application code mounting for development

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request


## 👥 Authors

- **TuyenLT** - *Initial work* - [tuyenlt](https://github.com/tuyenlt)

## 🙏 Acknowledgments

- FastAPI community for excellent documentation
- Clean Architecture principles by Robert C. Martin
- SQLAlchemy team for the powerful ORM

---

For more information, please refer to the [API Documentation](http://localhost:8000/docs) when the application is running.