.PHONY: help install start stop restart logs clean test

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make start      - Start all services"
	@echo "  make stop       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - Show logs"
	@echo "  make clean      - Clean up containers and volumes"
	@echo "  make test       - Run tests"

install:
	@echo "Installing dependencies..."
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	cd cli && pip install -e .

start:
	@echo "Starting services..."
	docker-compose up -d

stop:
	@echo "Stopping services..."
	docker-compose down

restart:
	@echo "Restarting services..."
	docker-compose restart

logs:
	docker-compose logs -f

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	rm -rf backend/__pycache__
	rm -rf frontend/node_modules
	rm -rf frontend/.next

test:
	@echo "Running tests..."
	cd backend && pytest
	cd frontend && npm test
