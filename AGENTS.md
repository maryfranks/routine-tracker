Agent Instructions

Quick Start / Commands
- `uv sync` — Install dependencies
- `uv run pytest` — Run the full test suite
- `uv run pytest tests/test_home.py` — Run a single test file

Core Rules
- Tooling Stack: Use `gh` for GitHub, `docker` for containers, `pytest` for testing.
- Dependencies: Dependencies must be added in `pyproject.toml`. Do not add one without asking.
- Direct Execution: Prefer direct shell execution (`gh`, `git`, `pytest`) over writing custom automation scripts for batch tasks.
- Don’t make assumptions. Ask questions when needed.

Documentation Index
- `_docs/process.md` — Agent workflow rules, execution preferences, and how work is organized.
- `_docs/testing-guidelines.md` — Read this before writing any tests.

Roles
- PM: refines a task before anyone implements it (following _docs/agent_roles/pm.md)
- Engineer: implements one refined task, (following _docs/agent_roles/software_engineer.md)
- QA: checks finished work against the issue acceptance criteria (following `_docs/agent_roles/qa.md`)

- Orchestration Loop:
  - The main session acts as the orchestrator, launching the software engineer and QA as subagents.
  - Lifecycle:
    1. Select the next open issue from the backlog.
    2. Engineer implements the issue.
    3. QA verifies the implementation.
    4. On FAIL, return to step 2 with the QA comment as input (maximum of 2 retry attempts).
    5. If the retry limit is reached without a PASS, halt execution and flag for human review.
    6. On PASS, close the issue.
    7. Repeat until the backlog is empty.
  - Rules:
    - The engineer does not close the issue.
    - QA does not modify code, only outputs PASS or FAIL.
    - The orchestrator closes the issue only after QA outputs PASS.