# Team & Agent Development Process

## 1. Task & Branch Workflow
- **One at a Time:** Pick up a single GitHub issue. Do not mix scopes.
- **Branching:** Always create a dedicated feature branch from `main` using the format `<issue-number>-<short-description>`.
- **Acceptance Criteria:** Read the issue criteria carefully before starting and verify them before opening a pull request.

## 2. Commit & Code Standards
- **Commit Regularly:** Make small, atomic commits with clear, descriptive messages. 
- **Simplicity First:** Do the simplest thing that works. Avoid over-engineering.
- **Python Style & Formatting:** Strict adherence to PEP 8. Code must be formatted and linted using **Ruff**.
- **Type Safety:** Full type hinting (`typing` module) is mandatory on all functions, methods, and classes. 
- **Pydantic Validation:** All request bodies, response payloads, and configuration settings must use Pydantic models with explicit field validation where applicable.


## 3. Verification
- Run the test suite (`uv run pytest`) and ensure all checks pass before submitting any code changes.