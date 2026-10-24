# ADR-001: Core Technology Stack Selection

## 1. Context & Problem Statement
We need to establish a robust, maintainable, and right-sized technology stack for the **Routine Tracker** MVP. As a portfolio project built on sound engineering principles, the architecture focuses on clean separation of concerns, secure data handling, and long-term extensibility without unnecessary over-engineering. The core requirements include:
* A modern, responsive user interface supporting a freeform board layout with potential for future mobile expansion.
* A clean, efficient backend API capable of handling secure authentication and business logic.
* A data layer that remains frictionless and lightweight for local development (SQLite) while maintaining database agnosticism for production cloud deployment (PostgreSQL).
* Pragmatic resource management and tooling aligned with developer familiarity to maximize delivery speed and maintainability.

## 2. Options Considered

### Frontend
* **React built with Vite** *(Selected)*
  * *Choice:* React provides a component-driven interface, and Vite serves as the modern build tool and development server for fast local compilation. 
  * *Rationale:* Keeps the interface cleanly separate from the backend API. React establishes a standard component model and leaves a clear path open if a mobile app version is desired later.
* **Full-Stack Framework (e.g., Next.js / Remix)**
  * *Rationale:* Bundling server-side rendering and combined routing adds unnecessary overhead for a focused single-page board interface.

### Backend
* **Python with FastAPI** *(Selected)*
  * *Rationale:* Aligns with recent development experience, offers fast performance, and automatically generates clean OpenAPI documentation for the API endpoints.
* **Node.js with Express**
  * *Rationale:* Skipped because Python and FastAPI align better with recent coding experience and personal preference.

### Database & Data Layer
* **SQLite for local development, utilizing an Object-Relational Mapper (ORM) targeting PostgreSQL in production** *(Selected)*
  * *Choice:* SQLite stores data in a lightweight local file, while an ORM acts as an abstraction layer to write database queries in Python rather than raw database language.
  * *Rationale:* SQLite requires zero local setup configuration for rapid early development. The ORM layer abstracts database calls so the same code maps smoothly to PostgreSQL when deployed.
* **Running PostgreSQL locally from day one**
  * *Rationale:* Skipped to avoid the friction of running local containerized databases during early feature development.

### Authentication
* **Secure, HTTP-only cookies storing JSON Web Tokens (JWTs)** *(Selected)*
  * *Choice:* JWTs securely represent user claims, and HTTP-only cookies prevent client-side JavaScript from reading the token.
  * *Rationale:* Provides right-sized security by protecting session tokens from client-side script access while integrating cleanly with FastAPI's native request handling.
* **External Identity Provider (e.g., Auth0, Keycloak, or AWS Cognito via OIDC/OAuth 2.0)**
  * *Rationale:* Skipped because delegating auth to a third-party service or dedicated enterprise server is complete overkill for a standalone portfolio project, adding unnecessary subscription costs, external network dependencies, and setup complexity.
* **Storing tokens in browser local storage**
  * *Rationale:* Skipped due to inherent security vulnerabilities regarding script exposure.

## 3. Decision & Rationale

We have selected a decoupled architecture utilizing a **React Single-Page Application (SPA) built with Vite** on the frontend, communicating via a **FastAPI** backend written in Python. 

* **For the Data Layer:** We are utilizing **SQLite** for frictionless local development paired with an **Object-Relational Mapper (ORM)**, ensuring a clean, abstracted migration path to **PostgreSQL** in production.
* **For Authentication:** We are implementing **JSON Web Tokens (JWTs)** stored securely in **HTTP-only cookies** managed directly by the FastAPI backend.

### Summary Rationale
This stack successfully hits our goal of "right-sized security" and robust engineering practices without falling into the trap of over-engineering. By choosing tools that align with recent development experience and avoiding enterprise-level infrastructure overhead (such as managed identity providers or local containerized databases from day one), we maintain rapid local iteration speed while ensuring the project remains clean, secure, and easily extensible for a professional portfolio.