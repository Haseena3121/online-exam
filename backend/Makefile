.PHONY: help install dev test clean docker-up docker-down migrate seed

help:
	@echo "Online Exam Proctoring System - Development Commands"
	@echo "===================================================="
	@echo "make install     - Install dependencies"
	@echo "make dev         - Start development server"
	@echo "make test        - Run tests"
	@echo "make clean       - Clean cache and temp files"
	@echo "make migrate     - Run database migrations"
	@echo "make seed        - Seed database with test data"
	@echo "make docker-up   - Start Docker containers"
	@echo "make docker-down - Stop Docker containers"

install:
	pip install -r requirements.txt

dev:
	python run.py

test:
	pytest --cov=. --cov-report=html

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	find . -type d -name '.coverage' -delete

migrate:
	flask db upgrade

seed:
	python seed_data.py

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f backend

docker-shell:
	docker-compose exec backend bash

lint:
	flake8 .
	pylint **/*.py

format:
	black .

requirements:
	pip freeze > requirements.txt