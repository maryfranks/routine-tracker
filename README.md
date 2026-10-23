# Routine Tracker

A modular, canvas-based habit tracker designed around flexible daily, weekly, and monthly cadences. Organize your routines into interactive, single-purpose tracking windows that live on a freeform board space, flip them over to inspect your historical consistency over time, and use data-driven insights to build sustainable habit stacks and correlate your daily well-being with your routines.

---

## 🚀 App Demo 🦖
*(Coming soon — visualizations and walkthroughs of the routine tracking interface will be added here once the MVP is built!)*

---

## 🚀 Getting Started & Local Development 🦖
*(Coming soon — instructions for local setup, environment variables, running the app, and executing the test suite will live here once the code and tech stack are established!)*

---

## 🚀 Project Structure 🦖
*(Coming soon — a detailed layout of the repository directories, code modules, and documentation files will be documented here!)*

---

## 🚀 Deployment 🦖
*(Coming soon — details on where and how the web application and database are hosted will be added here!)*

---

## 🚀 Repository Automations 🦖
*(Coming soon — information regarding CI/CD pipelines, automated testing workflows, and repo bots will be detailed here!)*

---

## 🤖 AI-Native Development & Agentic Workflow

This project is built using an intentional, structured **AI-native development methodology**, treating AI coding agents as specialized team members rather than general-purpose code generators. The workflow is designed to maximize resource efficiency, maintain architectural rigor, and prevent agent drift through strict guardrails.

### Core Pillars of the Workflow:

* **Strategic Model Selection & Resource Optimization:** 
  * Day-to-day planning, brainstorming, and scoping are conducted using lighter models via the web interface to conserve resources.
  * Purpose-built agent environments (such as Lovable/v0 for frontend prototyping, Codex for backend logic, and Gemini CLI for QA/non-coding loops) are deployed for specific implementation tasks.
  * Periodic audits are performed using heavier models to verify code quality and architectural integrity.
* **Specialized Agent Roles & Guardrails (`process.md`):** 
  * Agent personas (such as Product Manager, Engineer, and QA) are explicitly defined.
  * Operational guardrails and instructions are embedded in a dedicated `process.md` file to guide agents and eliminate repetitive corrections.
* **Hyper-Lean Context Engineering:** 
  * Documentation is broken down into small, targeted markdown files (such as PRDs and technical specs).
  * Agents only read the specific files required for their immediate task, relying on up-to-date specs rather than parsing massive codebases.
* **Controlled, Step-by-Step Execution Loops:** 
  * Work avoids massive, uncontrolled batch generation. 
  * Tasks are executed iteratively (e.g., executing a single GitHub issue, reviewing the output, updating documentation, and refining) before any automation loop is allowed to run autonomously.
* **Incremental Changes & Git Hygiene:** 
  * Code changes are kept small, modular, and highly testable.
  * Functionality and testability take precedence over rigid styling rules (such as strict Pydantic best practices or deep code style linting).
  * Frequent commits are made to ensure rapid review cycles and simple rollbacks.