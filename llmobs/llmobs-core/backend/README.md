# LLMObs Backend

FastAPI backend service with PostgreSQL, Redis, and Alembic migrations.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Database Services

```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Check status
docker-compose ps
```

### 4. Run Database Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Start the Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Management

### Create New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

### View Migration History

```bash
alembic history
```

## Models

The application includes these database models:

- **User** - User accounts with authentication
- **Organization** - Organizations owned by users
- **Plugin** - Plugins registered to organizations

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Users
- `GET /api/users/me` - Get current user
- `GET /api/users/{user_id}` - Get user by ID

### Gateway
- `GET /api/gateway/plugins` - List active plugins
- `ANY /api/gateway/{plugin_slug}/{path}` - Proxy to plugin services

## Testing

```bash
pytest
```

## Project Structure

```
backend/
├── alembic/              # Database migrations
│   ├── versions/         # Migration files
│   └── env.py           # Alembic environment
├── app/
│   ├── api/             # API routes
│   │   ├── auth.py      # Authentication endpoints
│   │   ├── users.py     # User endpoints
│   │   └── gateway.py   # Plugin gateway/proxy
│   ├── core/            # Core functionality
│   │   ├── config.py    # Configuration
│   │   └── db.py        # Database setup
│   ├── models/          # SQLAlchemy models
│   ├── services/        # Business logic
│   │   └── plugin_manager.py
│   └── main.py          # Application entry point
├── tests/               # Test files
├── alembic.ini          # Alembic configuration
├── requirements.txt     # Python dependencies
└── Dockerfile          # Docker image definition
```
