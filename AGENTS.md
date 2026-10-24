Agent Instructions

Quick Start / Commands
- `uv sync` — Install dependencies
- `uv run pytest` — Run the full test suite
- `uv run pytest tests/test_home.py` — Run a single test file

Core Rules
- Tooling Stack: Use `gh` for GitHub, `docker` for containers, `pytest` for testing.
- Dependencies: Dependencies must be added in `pyproject.toml`. Do not add one without asking.
- Direct Execution: Prefer direct shell execution (`gh`, `git`, `pytest`) over writing custom automation scripts for batch tasks.

Documentation Index
- `_docs/process.md` — Agent workflow rules, execution preferences, and how work is organized.
- `_docs/testing-guidelines.md` — Read this before writing any tests.