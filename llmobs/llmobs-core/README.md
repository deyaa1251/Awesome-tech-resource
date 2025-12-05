# LLMObs Core

A modular observability platform for LLM applications with plugin architecture.

## Architecture

LLMObs Core consists of three main components:

1. **Frontend** - React/Next.js host application with Module Federation
2. **Backend** - FastAPI core service with authentication and gateway
3. **CLI** - Command-line tool for managing the platform

## Features

- 🔌 Plugin Architecture with Module Federation
- 🔐 Authentication & Authorization
- 🚪 API Gateway with Reverse Proxy
- 📦 Plugin Management (install, start, list)
- 🐳 Docker-based deployment
- 💾 PostgreSQL & Redis support

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.9+

### Installation

```bash
# Install dependencies
make install

# Start all services
make start

# View logs
make logs
```

The services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Development

### Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### CLI Development

```bash
cd cli
pip install -e .
llmobs --help
```

## Project Structure

```
llmobs-core/
├── docker-compose.yml          # Orchestrates all services
├── Makefile                    # Development commands
├── frontend/                   # React/Next.js application
├── backend/                    # FastAPI service
└── cli/                        # CLI tool
```

## License

MIT
