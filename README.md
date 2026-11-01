# Routine Tracker

A modular, canvas-based habit tracker designed around flexible daily, weekly, and monthly cadences. Routines are organized into interactive, single-purpose tracking windows living on a freeform board space. Users can flip cards over to inspect historical consistency over time and leverage data-driven insights to build sustainable habit stacks and correlate daily well-being with established routines.

---

## 🚀 Application Demonstration (App Demo) 🦖

The Routine Tracker interface provides an interactive, canvas-based board for organizing and tracking daily, weekly, and monthly habits:

- **Routine Cards:** Single-purpose tracking windows residing on a freeform board space.
- **Card Flipping:** Individual routine cards flip to reveal historical consistency and completion analytics over time.
- **Views & Stacks:** Habits group into custom views for building sustainable habit stacks.

*(Screenshots of the running application interface will be added here once captured from the local development environment).*

---

## 🚀 Getting Started & Local Development 🦖

Follow these steps to set up and run Routine Tracker locally.

### Prerequisites
- **Python (>= 3.10)** with **uv** installed for backend package management.
- **Bun** (>= 22.0.0 / 1.4.4+) installed for frontend package management.

### 1. Install Dependencies
Install dependencies for both backend and frontend from the repository root:
```bash
# Install backend dependencies
make backend-install
# or: uv sync

# Install frontend dependencies
make frontend-install
# or: bun --cwd frontend install
```

### 2. Run the Application Locally
Run the backend and frontend development servers in two separate terminal windows from the repository root:

* **Terminal 1: Backend Server**
  ```bash
  make backend-dev
  # or: uv run uvicorn backend.main:app --reload
  ```
  The Python FastAPI backend application programming interface (API) is available at `http://localhost:8000` (with interactive documentation at `/docs`).

* **Terminal 2: Frontend Development Server**
  ```bash
  make frontend-dev
  # or: bun --cwd frontend run dev -- --host
  ```
  The Vite frontend development server is available at `http://localhost:5173`.

### 3. Running Tests
* **Backend Tests:**
  ```bash
  make backend-test
  # or: uv run pytest
  ```
* **Frontend Tests:**
  ```bash
  make frontend-test
  # or: bun --cwd frontend test
  ```

---

## 🚀 Project Structure 🦖

The repository is organized into a modular backend-frontend architecture:

```text
/workspaces/routine-tracker/
├── backend/              # Python FastAPI backend API and routers
│   ├── models/           # SQLAlchemy Object-Relational Mapper (ORM) models (Task, User, View, CompletionLog)
│   ├── routers/          # API endpoint routers (auth, tasks, views, clock, history)
│   └── tests/            # Pytest test suite
├── frontend/             # React + Vite frontend application (TanStack Router, shadcn/ui)
│   └── src/
│       ├── components/   # User Interface (UI) components and routine widgets
│       ├── hooks/        # React Query hooks and custom state logic
│       ├── lib/          # Period calculations, error handling, and utilities
│       └── routes/       # File-based routing (index, history, login)
└── _docs/                # Architecture specifications, Architecture Decision Records (ADRs), and agent roles
```

---

## 🚀 Deployment 🦖

- **Database:** SQLite (`dev.db`) for local development, with SQLAlchemy ORM abstraction supporting PostgreSQL for production deployment.
- **Backend:** Python FastAPI server container or service deployment.
- **Frontend:** Static asset build generated via Vite (`bun run build`), deployable on modern static hosting platforms or served alongside the backend.

---

## 🚀 Repository Automations 🦖

Routine Tracker utilizes a standardized `Makefile` to orchestrate build, development, and testing workflows:

- **Dependencies:** `make backend-install` (`uv sync`) and `make frontend-install` (`bun install`).
- **Development Servers:** `make backend-dev` (FastAPI with reload) and `make frontend-dev` (Vite dev server).
- **Test Suites:** `make backend-test` (`uv run pytest`) and `make frontend-test` (`bun test`).
- **Code Quality:** Frontend linting (`make frontend-lint`) and formatting (`make frontend-format` with Prettier).

---

## 🤖 AI-Native Development & Agentic Workflow

This project is built using an intentional, structured artificial intelligence (AI)-native development methodology, treating AI coding agents as specialized team members rather than general-purpose code generators. The workflow maximizes resource efficiency, maintains architectural rigor, and prevents agent drift through strict guardrails.

### Core Pillars of the Workflow:

* **Strategic Model Selection & Resource Optimization:** 
  * Day-to-day planning, brainstorming, and scoping utilize lighter models via the web interface to conserve resources.
  * Purpose-built agent environments (such as Lovable/v0 for frontend prototyping, Codex for backend logic, and Gemini Command Line Interface (CLI) for quality assurance (QA)/non-coding loops) deploy for specific implementation tasks.
  * Periodic audits using heavier models verify code quality and architectural integrity.
* **Specialized Agent Roles & Guardrails (`process.md`):** 
  * Agent personas (such as Product Manager (PM), Software Engineer (SWE), and QA) are explicitly defined.
  * Operational guardrails and instructions embed in a dedicated `process.md` file to guide agents and eliminate repetitive corrections.
* **Hyper-Lean Context Engineering:** 
  * Documentation breaks down into small, targeted markdown files (such as product requirements documents (PRDs) and technical specifications).
  * Agents read only the specific files required for immediate tasks, relying on up-to-date specifications rather than parsing massive codebases.
* **Controlled, Step-by-Step Execution Loops:** 
  * Work avoids massive, uncontrolled batch generation. 
  * Tasks execute iteratively (such as executing a single GitHub issue, reviewing output, updating documentation, and refining) before permitting autonomous execution loops.
* **Incremental Changes & Git Hygiene:** 
  * Code changes remain small, modular, and highly testable.
  * Functionality and testability take precedence over rigid styling rules (such as strict Pydantic best practices or deep code style linting).
  * Frequent commits ensure rapid review cycles and simple rollbacks.