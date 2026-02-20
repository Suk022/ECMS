# Eye Clinic Management System

A role-based, full-stack web application to digitize and streamline the end-to-end workflow of an eye clinic — from appointment booking to treatment completion.

---


## What is this project?

Small eye clinics often run on paper registers, phone calls, and disconnected tools to manage appointments, patient records, and billing. This leads to scheduling conflicts, lost patient history, missed follow-ups, and poor coordination between doctors and front desk staff.

**ECMS** is a centralized digital platform built to solve exactly that. It brings the **doctor, receptionist, and patient** into one structured system where every step of a clinical visit — from request to treatment — is tracked, communicated, and recorded.

---

## Who uses it?

| Role | What they do |
|---|---|
|  **Doctor** | Manages appointments, records prescriptions, sets billing, marks treatment complete |
|  **Receptionist** | Confirms payments, views billing and prescriptions |
|  **Patient** | Books appointments, receives real-time notifications |

---

## Core Features

### Doctor
- View all appointment requests with real-time status
- **Approve** or **reject** appointments — rejections include a written note sent directly to the patient
- Overdue/pending appointments from past days are **highlighted separately**
- Record consultation notes and prescriptions (medications, dosages, instructions)
- Set billing amount for each visit
- Mark patient as **treated** — automatically archives to history and sends completion message

### Receptionist
- View all billing records created by the doctor
- Access linked prescriptions for payment reference
- Confirm payment received → **triggers patient reminder notification**

### Patient
- Register profile and submit appointment requests
- Receive structured notifications at every stage:
  - Appointment confirmed
  - Appointment rejected (with doctor's note)
  - Reminder (sent once payment is confirmed)
  - Treatment completion message

---

## How it works — The Workflow

```
Patient submits appointment request
          │
          ▼
 Doctor reviews request
    │               │
  APPROVE         REJECT (with note)
    │               │
    │         Patient notified
    ▼
Doctor consults patient
    │
    ▼
Doctor records prescription + sets billing amount
    │
    ▼
Receptionist confirms payment received
    │
    ▼
System sends reminder to patient
    │
    ▼
Doctor marks patient as TREATED
    │
    ▼
Appointment archived to history + completion message sent
```

---

## Data Model (Overview)

Six core tables power the system:

```
users ──────────── patients (profile extension)
  │
  └── appointments (central entity)
          │
          ├── prescriptions
          ├── billing
          └── notifications
```

Every record in the system connects back to an **appointment** — this is intentional. A visit is the core unit of clinic workflow.

**Appointment lifecycle states:** `REQUESTED → APPROVED → TREATED` or `REQUESTED → REJECTED`

**Billing states:** `PENDING → PAID`

---

## Tech Stack

**Frontend:** React with TailwindCSS for responsive UI and styling.

**Backend:** FastAPI (Python) for building RESTful APIs with high performance and automatic validation.

**Database:** PostgreSQL as the relational database for persistent data storage.

**ORM & Migrations:** SQLAlchemy for ORM-based database interaction, with Alembic for schema migrations and version control.

**Authentication & Authorization:** JWT-based authentication with role-based access control (RBAC).

**Notifications:** SendGrid for email notifications and Twilio for SMS messaging.

---

## Scope & Roadmap

This project is being built in phases:

- **Phase 1** — Project setup, database models, authentication system
- **Phase 2** — Core appointment workflow APIs (approve, reject, prescribe, bill, treat)
- **Phase 3** — Role-based frontend dashboards (Doctor, Receptionist, Patient)
- **Phase 4** — Notification engine, patient history view, UI polish
- **Phase 5** *(planned)* — Analytics, online payments, multi-doctor support

> **This project is currently under active development.** This README will be updated as each phase is completed.

---

## Why this project?

This is a self-designed, self-scoped full-stack project. Every design decision (schema, workflow, role logic) was thought through from first principles. The goal is to build something that mirrors how real clinic software works, and document the process along the way.

---
