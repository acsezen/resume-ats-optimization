# AI Resume Builder MVP - Makefile
# Development and deployment commands using uv

.PHONY: help install dev test lint format clean run build docker

# Default target
help:
	@echo "🤖 AI Resume Builder MVP - Development Commands"
	@echo "================================================"
	@echo ""
	@echo "Setup Commands:"
	@echo "  install     Install dependencies with uv"
	@echo "  dev         Install with dev dependencies"
	@echo ""
	@echo "Development Commands:"
	@echo "  run         Start the development server"
	@echo "  test        Run the test suite"
	@echo "  lint        Run linting checks"
	@echo "  format      Format code with black and isort"
	@echo "  type-check  Run mypy type checking"
	@echo ""
	@echo "Maintenance Commands:"
	@echo "  clean       Clean up temporary files"
	@echo "  update      Update dependencies"
	@echo "  build       Build the package"
	@echo ""
	@echo "Docker Commands:"
	@echo "  docker      Build and run with Docker"
	@echo ""
	@echo "Usage Examples:"
	@echo "  make install              # Install dependencies"
	@echo "  make dev                  # Setup development environment"
	@echo "  make run                  # Start the server"
	@echo "  OPENAI_API_KEY=xxx make run  # Run with AI features"

# Installation commands
install:
	@echo "📦 Installing dependencies with uv..."
	uv sync --no-editable

dev:
	@echo "🛠️  Installing development dependencies..."
	uv sync --no-editable --all-extras

# Development commands
run:
	@echo "🚀 Starting AI Resume Builder MVP..."
	@echo "💡 Tip: Set OPENAI_API_KEY environment variable to enable AI features"
	uv run python main.py

test:
	@echo "🧪 Running test suite..."
	uv run pytest tests/ -v --cov=. --cov-report=term-missing

test-sample:
	@echo "🧪 Running sample tests..."
	uv run python test_sample.py

lint:
	@echo "🔍 Running linting checks..."
	uv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	uv run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics

format:
	@echo "🎨 Formatting code..."
	uv run black . --line-length=100
	uv run isort . --profile=black --line-length=100

type-check:
	@echo "🔍 Running type checks..."
	uv run mypy . --ignore-missing-imports

# Quality checks (run all)
check: lint type-check test
	@echo "✅ All quality checks completed"

# Maintenance commands
clean:
	@echo "🧹 Cleaning up temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf build/ dist/ .coverage htmlcov/

update:
	@echo "🔄 Updating dependencies..."
	uv sync --upgrade

build:
	@echo "📦 Building package..."
	uv build

# Docker commands
docker:
	@echo "🐳 Building and running with Docker..."
	docker build -t ai-resume-builder-mvp .
	docker run -p 8000:8000 -e OPENAI_API_KEY="${OPENAI_API_KEY}" ai-resume-builder-mvp

# Development workflow
dev-setup: clean install dev
	@echo "🎉 Development environment ready!"
	@echo "Run 'make run' to start the server"

# Production deployment
deploy-check: clean install test lint type-check
	@echo "✅ Ready for deployment"

# Show project info
info:
	@echo "📊 Project Information"
	@echo "====================="
	@echo "Project: AI Resume Builder MVP"
	@echo "Python: $(shell python --version)"
	@echo "uv: $(shell uv --version)"
	@echo "Dependencies: $(shell uv pip list | wc -l) packages"
	@echo ""
	@echo "🌐 URLs:"
	@echo "  Local: http://localhost:8000"
	@echo "  Builder: http://localhost:8000/builder"
	@echo "  Analyzer: http://localhost:8000/analyzer"

# Quick start for new developers
quickstart:
	@echo "🚀 Quick Start for AI Resume Builder MVP"
	@echo "========================================"
	@echo ""
	@echo "1. Install uv (if not already installed):"
	@echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
	@echo ""
	@echo "2. Set up development environment:"
	@echo "   make dev-setup"
	@echo ""
	@echo "3. (Optional) Set OpenAI API key for AI features:"
	@echo "   export OPENAI_API_KEY='your-api-key'"
	@echo ""
	@echo "4. Start the development server:"
	@echo "   make run"
	@echo ""
	@echo "5. Open http://localhost:8000 in your browser"
	@echo ""
	@echo "For more commands, run: make help"