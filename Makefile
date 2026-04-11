.PHONY: install dev test lint typecheck run migrate seed clean

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	python -m pytest tests/ -v --tb=short

test-cov:
	python -m pytest tests/ -v --cov=app --cov-report=term-missing

lint:
	python -m ruff check app/ tests/
	python -m ruff format --check app/ tests/

lint-fix:
	python -m ruff check --fix app/ tests/
	python -m ruff format app/ tests/

typecheck:
	python -m mypy app/

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

migrate:
	alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m "$(msg)"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
