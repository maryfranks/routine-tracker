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
	cd frontend && bun install

frontend-dev:
	cd frontend && bun run dev -- --host

frontend-build:
	cd frontend && bun run build

frontend-preview:
	cd frontend && bun run preview

frontend-test:
	cd frontend && bun test

frontend-lint:
	cd frontend && bun run lint

frontend-format:
	cd frontend && bun run format

# --- Backend Commands ---
backend-install:
	uv sync

backend-dev:
	uv run uvicorn backend.main:app --reload

backend-test:
	uv run pytest
