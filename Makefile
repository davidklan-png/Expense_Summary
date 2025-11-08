.PHONY: help install format lint test test-cov type-check security clean

help:  ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install all dependencies
	poetry install

format:  ## Format code with black and isort
	poetry run black .
	poetry run isort .

lint:  ## Run all linters (ruff)
	poetry run ruff check .

lint-fix:  ## Run linters with auto-fix
	poetry run ruff check --fix .

test:  ## Run tests with basic quality checks (recommended before commit)
	@echo "=== Running tests with quality checks ==="
	@echo ""
	@echo "Formatting code..."
	@$(MAKE) format
	@echo ""
	@echo "Running linters..."
	@$(MAKE) lint
	@echo ""
	@echo "Running tests..."
	poetry run pytest
	@echo ""
	@echo "✅ All checks passed! Safe to commit."

test-only:  ## Run tests only (fast, no formatting/linting)
	poetry run pytest

test-cov:  ## Run tests with coverage report
	poetry run pytest --cov=saisonxform --cov-report=html --cov-report=term-missing

test-watch:  ## Run tests in watch mode
	poetry run pytest-watch

type-check:  ## Run type checking with mypy
	poetry run mypy src/saisonxform

security:  ## Run security scan with bandit
	poetry run bandit -r src/saisonxform -ll

qa:  ## Run all quality checks (format, lint, type-check, security, test)
	@echo "Running code formatting..."
	@$(MAKE) format
	@echo "\nRunning linters..."
	@$(MAKE) lint
	@echo "\nRunning type checks..."
	@$(MAKE) type-check
	@echo "\nRunning security scan..."
	@$(MAKE) security
	@echo "\nRunning tests..."
	@$(MAKE) test-cov

ci:  ## Simulate CI checks locally (matches GitHub Actions exactly)
	@echo "=== Running CI checks locally (GitHub Actions simulation) ==="
	@echo ""
	@echo "1/5 Code Quality - Black formatting..."
	poetry run black --check .
	@echo ""
	@echo "2/5 Code Quality - isort import sorting..."
	poetry run isort --check-only .
	@echo ""
	@echo "3/5 Code Quality - Ruff linting..."
	poetry run ruff check .
	@echo ""
	@echo "4/5 Type Checking - mypy (errors allowed)..."
	poetry run mypy src/saisonxform || true
	@echo ""
	@echo "5/5 Tests - pytest with coverage..."
	poetry run pytest --cov=saisonxform --cov-report=xml --cov-report=term-missing
	@echo ""
	@echo "✅ All CI checks completed!"
	@echo ""
	@echo "Note: Type checking and security warnings are informational only."
	@echo "GitHub Actions will PASS as long as Black, isort, Ruff, and tests succeed."

clean:  ## Clean build artifacts and caches
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

pre-commit-install:  ## Install pre-commit hooks
	poetry run pre-commit install
	poetry run pre-commit install --hook-type commit-msg

pre-commit-run:  ## Run pre-commit hooks on all files
	poetry run pre-commit run --all-files

update-deps:  ## Update dependencies
	poetry update

lock:  ## Update poetry.lock file
	poetry lock --no-update
