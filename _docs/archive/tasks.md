# Routine Tracker MVP - Task Backlog

This document contains the complete, modular backlog of tasks for the Routine Tracker application, formatted as self-contained units for AI coding agent execution.

---

# Section 1: Initial Bootstrapping Work

## Lovable Frontend Ingestion & Setup
Goal: Ingest and configure the pre-generated Lovable frontend shell containing mock data into the repository.
Description: Place the Lovable-generated UI code into the `frontend/` directory, preserving existing mock data structures to maintain the established visual target. Verify Vite build configurations in `frontend/vite.config.ts` and ensure package dependencies in `frontend/package.json` are installed correctly.

## OpenAPI Specification Authoring
Goal: Author the definitive OpenAPI specification governing all REST endpoints for the routine management application.
Description: Create a comprehensive `openapi.yaml` file in the repository root detailing all authentication, custom view, task management, and logging endpoints based on the Lovable frontend UI requirements. This file will serve as the strict contract for both the FastAPI backend implementation and API client integration.

## Backend FastAPI Skeleton and Smoke Test
Goal: Establish the Python FastAPI backend project skeleton with a verified test runner and smoke test endpoint.
Description: Initialize the `backend/` directory with a standard layout including `backend/main.py`, `backend/requirements.txt`, and a `backend/tests/` folder. Implement a basic health-check smoke test in `backend/tests/test_smoke.py` runnable via pytest to validate the server startup and test pipeline.

## Database Schema and ORM Configuration
Goal: Configure the SQLAlchemy ORM data abstraction layer and database connection setup for SQLite and PostgreSQL.
Description: Create `backend/database.py` to manage database session lifecycle and environment-based connection strings. Implement foundational database models in `backend/models/` for users, views, tasks, and completion logs in alignment with the SQLite development and PostgreSQL production requirements.

## Backend Middleware and Router Stubs
Goal: Configure backend CORS policies, secure HTTP-only cookie authentication handling, and API router stubs.
Description: Configure CORS rules, error handling, and security middleware inside `backend/main.py`. Establish initial router stub files under `backend/routers/` corresponding to the tags defined in `openapi.yaml` to enable modular endpoint implementation.

---

# Section 2: All Tasks Necessary for the MVP

## User Authentication & Session Management Endpoints
Goal: Implement secure user registration, login, logout, and session validation endpoints with HTTP-only cookies.
Description: Implement authentication routes in `backend/routers/auth.py` adhering to the paths defined in `openapi.yaml`. Use secure, HTTP-only JWT cookies for session handling and integrate with the user models in `backend/models/user.py`.

## Custom Views CRUD API Implementation
Goal: Build backend REST endpoints for creating, reading, editing, and deleting custom views with cadence assignments.
Description: Implement view management routes in `backend/routers/views.py` matching `openapi.yaml` specifications. Ensure business logic validates daily, weekly, and monthly recurrence types against the database models in `backend/models/view.py`.

## Task Management CRUD API Implementation
Goal: Implement backend REST endpoints for managing tasks strictly tied to single custom views with binary completion states.
Description: Create task management routes in `backend/routers/tasks.py` conforming to `openapi.yaml`. Enforce one-to-one view relationships and binary done/not-done status handling using ORM models in `backend/models/task.py`.

## Task Completion and Reset Logic
Goal: Implement task completion tracking and period-based reset logic without rollover mechanics.
Description: Implement completion logging endpoints in `backend/routers/logs.py` as defined in `openapi.yaml`. Ensure that uncompleted tasks reset cleanly at the end of daily, weekly, or monthly periods without accumulating or rolling over into overdue states.

## Historical Completion Logging API
Goal: Provide historical completion logs and timeline retrieval endpoints for unlimited past periods.
Description: Implement history retrieval routes in `backend/routers/history.py` based on `openapi.yaml`. Query completion log tables in the database to return historical records of completed versus uncompleted periods for user review.

## Frontend API Client Wiring & Mock Replacement
Goal: Replace frontend mock data layers with live API calls matching the generated `openapi.yaml` contracts.
Description: Update frontend service or API client modules in `frontend/src/services/` or `frontend/src/api/` to communicate with the FastAPI backend endpoints. Wire the Lovable-generated UI components to consume real data while preserving the existing UI structure and visual presentation.

---

# Section 3: Nice-to-Haves (Post-MVP)

## Multi-User Sharing and Collaborative Households
Goal: Extend backend models and frontend views to support multi-user household collaboration and shared routines.
Description: Update database schemas in `backend/models/` to support household sharing permissions and relational user mappings. Add corresponding endpoints in `openapi.yaml` and router extensions in `backend/routers/households.py` to manage shared access.

## Rigid Scheduling and Calendar Date Rules
Goal: Introduce rigid calendar-based scheduling options alongside floating cadence targets.
Description: Expand view and task models in `backend/models/` to support specific calendar recurrence rules (e.g., every Monday, 1st of the month). Update scheduling logic in backend services and adapt frontend UI components to configure rigid date rules.

## Task Duplication and Cross-View Sharing
Goal: Enable tasks to be duplicated or shared across multiple custom views.
Description: Refactor database schemas in `backend/models/task.py` from a strict one-to-one relationship to a many-to-many association table linking tasks and views. Update backend CRUD routers in `backend/routers/tasks.py` to handle shared task assignments.

## Advanced Statistics, Completion Percentages, and Streaks
Goal: Implement analytics engines to calculate completion percentages, historical streaks, and advanced productivity statistics.
Description: Create analytics and reporting endpoints in `backend/routers/analytics.py` referencing historical completion logs in the database. Implement corresponding visualization components within the frontend UI to display user streaks and stats.