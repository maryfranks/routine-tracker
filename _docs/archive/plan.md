# Routine Management App - MVP Scope & Product Definition

This document outlines the complete product scope for the Minimum Viable Product (MVP) of your routine management web application.

---

## 1. Core Architecture & Access
* **Platform:** Web application accessed via browser.
* **Authentication:** Secure user login and authentication system.
* **Data Persistence:** Backed by a proper database to ensure user data persists securely across devices and sessions.
* **User Model:** Single-user app for the MVP (multi-user sharing/households reserved for a future phase).

---

## 2. Views System
* **Custom Views:** Users can create, edit, and delete their own custom views (e.g., "Health", "Home", "Work").
* **Cadence Assignment:** When a user creates a new view, they must select its recurrence type:
  * **Daily**
  * **Weekly**
  * **Monthly**
* **Default State:** New accounts start with zero views by default.

---

## 3. Task Management
* **View Relationship:** Each task is strictly tied to a single view (one-to-one relationship). Tasks do not cross over multiple views in the MVP.
* **Floating Targets:** Tasks operate on floating schedules rather than rigid calendar days (e.g., completed 1x per day, 1x per week, or 1x per month).
* **Binary Completion:** Task status is strictly **done or not done** for the current active period.
* **No Rollover:** At the end of a period (e.g., end of the day, week, or month), uncompleted tasks reset cleanly. They do not accumulate, roll over, or show as overdue.

---

## 4. History & Logging
* **Historical Tracking:** Users can view their past completion history over an unlimited timeline ("forever").
* **Log View:** Past logs show historical records of completed versus uncompleted periods.
* **Exclusions:** High-level analytics, streaks, and advanced stats are intentionally omitted for the MVP and deferred to a future update.

---

## 5. Future Roadmap (Post-MVP)
The following features have been explicitly scoped out of the MVP to keep development focused, but are noted for future iterations:
* Multi-user sharing and collaborative households.
* Rigid scheduling (e.g., "every Monday" or "the 1st of every month").
* Task duplication or sharing across multiple views.
* Advanced statistics, completion percentages, and streak tracking.