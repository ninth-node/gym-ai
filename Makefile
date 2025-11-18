.PHONY: help install dev build up down logs clean test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies for both frontend and backend
	cd frontend && npm install
	cd backend && pip install -r requirements.txt

dev: ## Start development environment with Docker Compose
	docker-compose up

build: ## Build Docker images
	docker-compose build

up: ## Start all services in detached mode
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

clean: ## Remove all containers, volumes, and build artifacts
	docker-compose down -v
	rm -rf frontend/node_modules frontend/.next
	rm -rf backend/__pycache__ backend/**/__pycache__

test-frontend: ## Run frontend tests
	cd frontend && npm run test

test-backend: ## Run backend tests
	cd backend && pytest

test: test-frontend test-backend ## Run all tests

migrate: ## Run database migrations
	docker-compose exec backend alembic upgrade head

migrate-create: ## Create a new migration (usage: make migrate-create MESSAGE="message")
	docker-compose exec backend alembic revision --autogenerate -m "$(MESSAGE)"

shell-backend: ## Open a shell in the backend container
	docker-compose exec backend /bin/bash

shell-frontend: ## Open a shell in the frontend container
	docker-compose exec frontend /bin/sh

db-shell: ## Open PostgreSQL shell
	docker-compose exec db psql -U postgres -d gym_ai

redis-cli: ## Open Redis CLI
	docker-compose exec redis redis-cli

restart: ## Restart all services
	docker-compose restart

status: ## Show status of all services
	docker-compose ps
