.PHONY: help frontend-install frontend-dev frontend-build frontend-preview frontend-test frontend-lint frontend-format backend-install backend-dev backend-test

.DEFAULT_GOAL := help

help:
	@echo "Routine Tracker - Commands:"
	@echo ""
	@echo "Frontend:"
	@echo "  make frontend-install   - Install frontend dependencies (bun install)"
	@echo "  make frontend-dev       - Run frontend development server (bun run dev)"
	@echo "  make frontend-build     - Build frontend for production (bun run build)"
	@echo "  make frontend-preview   - Preview production build (bun run preview)"
	@echo "  make frontend-test      - Run frontend tests (bun test)"
	@echo "  make frontend-lint      - Lint frontend code (bun run lint)"
	@echo "  make frontend-format    - Format frontend code with Prettier (bun run format)"
	@echo ""
	@echo "Backend:"
	@echo "  make backend-install    - Install backend dependencies (uv sync)"
	@echo "  make backend-dev        - Run backend development server (uv run uvicorn)"
	@echo "  make backend-test       - Run backend tests (uv run pytest)"

# --- Frontend Commands ---
frontend-install:
	bun install --cwd frontend

frontend-dev:
	bun run --cwd frontend dev -- --host

frontend-build:
	bun run --cwd frontend build

frontend-preview:
	bun run --cwd frontend preview

frontend-test:
	bun run --cwd frontend test

frontend-lint:
	bun run --cwd frontend lint

frontend-format:
	bun run --cwd frontend format

# --- Backend Commands ---
backend-install:
	uv sync

backend-dev:
	uv run uvicorn backend.main:app --reload

backend-test:
	uv run pytest
