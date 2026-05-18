# Prompt 01 — ARCHIE: Database Model & Schemas (Commit B1)

**Date**: 2026-05-17  
**Agent**: ARCHIE (Database & Architecture)  
**Branch**: `feature/backend`  
**Commit**: B1 — `feat(backend): add employee model, database config, and pydantic schemas`

---

## Sub-Agent Task Prompt

This is the exact prompt given to the ARCHIE sub-agent in the Antigravity Agent Manager:

```
You are ARCHIE, the Database Architect agent in the aGi squad.

Task: Set up the database layer for a salary management system (FastAPI + SQLite + SQLAlchemy).

MANDATORY: Follow strict TDD — write the failing tests FIRST, then implement.

## Step 1 — RED (write failing tests)
Create `tests/test_schemas.py` with these test cases BEFORE any implementation:
- test_valid_employee_create_passes_validation
- test_full_name_is_required
- test_email_is_required
- test_negative_salary_is_rejected
- test_zero_salary_is_rejected
- test_currency_defaults_to_usd
- test_full_name_cannot_be_empty_string
- test_country_is_required
- test_employee_update_all_fields_optional
- test_employee_update_partial_salary
- test_employee_update_rejects_negative_salary
- test_employee_response_includes_id
- test_employee_response_serializes_to_dict

Run pytest — confirm all tests FAIL before writing implementation.

## Step 2 — GREEN (implement to pass tests)
Create these files:
1. `app/database.py` — SQLAlchemy engine (SQLite), session factory, DeclarativeBase, get_db dependency
2. `app/models/employee.py` — Employee ORM model with:
   - id (PK, autoincrement)
   - full_name (VARCHAR 200, NOT NULL)
   - email (VARCHAR 254, UNIQUE, NOT NULL)
   - job_title (VARCHAR 100, NOT NULL, indexed)
   - department (VARCHAR 100, NOT NULL)
   - country (VARCHAR 100, NOT NULL, indexed)
   - salary (Numeric 12,2 — positive only via CheckConstraint)
   - currency (VARCHAR 3, default USD)
   - hire_date (Date, NOT NULL)
   - created_at, updated_at (DateTime, auto-managed)
   - Composite index on (country, job_title) for analytics queries
3. `app/schemas/employee.py` — Pydantic v2 schemas:
   - EmployeeCreate (all required except currency)
   - EmployeeUpdate (all optional for partial updates)
   - EmployeeResponse (from_attributes=True for ORM serialization)
   - PaginatedEmployeeResponse
4. `tests/conftest.py` — shared fixtures:
   - In-memory SQLite engine (sqlite:///:memory:)
   - Session with rollback isolation per test
   - TestClient with get_db dependency override

## Step 3 — REFACTOR
Use FastAPI lifespan context manager (not deprecated on_event).
Run pytest again — all 13 tests must pass in < 1 second.

## Constraints
- Pydantic v2 syntax (model_config, ConfigDict, field_validator)
- Foreign keys enabled via PRAGMA
- Type annotations on all functions
- Docstrings on all modules and classes
```

---

## Key AI Decisions

1. **Chose `Numeric(12,2)` over `Float`** — avoids floating-point rounding errors in salary calculations
2. **Composite index `(country, job_title)`** — serves the primary analytics query `avg salary for role X in country Y` in a single index scan
3. **CheckConstraint at DB level** — belt-and-suspenders with Pydantic validation; DB rejects invalid data even if the API layer is bypassed
4. **Session rollback instead of table truncation** — faster test isolation, no DDL overhead per test
5. **`lifespan` over `on_event`** — `on_event` is deprecated in FastAPI 0.95+; `lifespan` is the modern async context manager pattern

## Test Results

```
13 passed in 0.02s
```

## Manual Corrections Applied

- None — implementation passed tests on first attempt after refactor
