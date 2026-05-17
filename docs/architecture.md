# Architecture Overview

## System Architecture

```
┌─────────────────┐        HTTP/JSON         ┌─────────────────┐
│                 │ ◄──────────────────────►  │                 │
│  Next.js 14     │                           │  FastAPI         │
│  (Frontend)     │                           │  (Backend)       │
│                 │                           │                 │
│  - TypeScript   │                           │  - SQLAlchemy   │
│  - Tailwind CSS │                           │  - Pydantic     │
│  - shadcn/ui    │                           │  - SQLite       │
│                 │                           │                 │
│  Port: 3000     │                           │  Port: 8000     │
└─────────────────┘                           └────────┬────────┘
                                                       │
                                                       │ SQLAlchemy ORM
                                                       │
                                              ┌────────▼────────┐
                                              │                 │
                                              │  SQLite DB      │
                                              │  (File-based)   │
                                              │                 │
                                              └─────────────────┘
```

## Backend Layers

```
HTTP Request
    │
    ▼
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Router  │ ──► │ Schema   │ ──► │ Service  │ ──► │  Model   │
│ (API)    │     │ (Valid.) │     │ (Logic)  │     │  (ORM)   │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
```

- **Router**: Handles HTTP concerns (status codes, path params, query params)
- **Schema**: Validates & transforms data (Pydantic models)
- **Service**: Contains business logic (testable without HTTP)
- **Model**: SQLAlchemy ORM models (database representation)

## Key Design Decisions

1. **Service layer separation** — Business logic lives in services, NOT in routes. This makes the core logic testable without spinning up HTTP.

2. **In-memory test database** — Tests use `sqlite:///:memory:` for speed and isolation. No test data leaks between runs.

3. **Bulk insert for seeding** — `executemany()` over individual `session.add()` for ~10x performance gain.

4. **CORS configured for development** — Restricted to `localhost:3000`. Must be updated for production domain.

## Data Model

See [Employee Model](../backend/app/models/employee.py) for the full schema.

Key indexes:
- `idx_employee_country` — Country-based analytics queries
- `idx_employee_job_title` — Job-title analytics queries
- `idx_employee_country_job_title` — Combined analytics queries
