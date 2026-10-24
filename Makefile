.PHONY: help frontend-install frontend-dev backend-install backend-dev

.DEFAULT_GOAL := help

help:
	@echo "Routine Tracker - Commands:"
	@echo ""
	@echo "Frontend:"
	@echo "  make frontend-install  - Install frontend dependencies"
	@echo "  make frontend-dev      - Run frontend development server"
	@echo ""
	@echo "Backend (Coming soon):"
	@echo "  make backend-install   - Install backend dependencies"
	@echo "  make backend-dev       - Run backend development server"

# --- Frontend Commands ---
frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

# --- Backend Commands (Placeholder) ---
backend-install:
	@echo "Backend install command not configured yet."
	# Example for later: uv sync

backend-dev:
	@echo "Backend dev command not configured yet."
	# Example for later: uv run uvicorn backend.main:app --reload
