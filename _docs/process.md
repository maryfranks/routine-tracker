# Team & Agent Development Process

## 1. Task & Branch Workflow
- **One at a Time:** Pick up a single GitHub issue. Do not mix scopes.
- **Branching:** Always create a dedicated feature branch from `main` using the format `<issue-number>-<short-description>`.
- **Acceptance Criteria:** Read the issue criteria carefully before starting and verify them before opening a pull request.

## 2. Commit & Code Standards
- **Commit Regularly:** Make small, atomic commits with clear, descriptive messages. 
- **Simplicity First:** Do the simplest thing that works. Avoid over-engineering.


## 3. Verification
- Run the test suite (`uv run pytest`) and ensure all checks pass before submitting any code changes.