.PHONY: help frontend-install frontend-dev frontend-build frontend-preview frontend-test frontend-lint frontend-format backend-install backend-dev

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
	@echo "Backend (Coming soon):"
	@echo "  make backend-install    - Install backend dependencies"
	@echo "  make backend-dev        - Run backend development server"

# --- Frontend Commands ---
frontend-install:
	cd frontend && bun install

frontend-dev:
	cd frontend && bun run dev

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

# --- Backend Commands (Placeholder) ---
backend-install:
	@echo "Backend install command not configured yet."
	# Example for later: uv sync

backend-dev:
	@echo "Backend dev command not configured yet."
	# Example for later: uv run uvicorn backend.main:app --reload
