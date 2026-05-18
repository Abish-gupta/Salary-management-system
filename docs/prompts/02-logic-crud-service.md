# Prompt 02 — LOGIC: Employee CRUD Service (Commit B2)

**Date**: 2026-05-17  
**Agent**: LOGIC (Backend Engineer)  
**Branch**: `feature/backend`  
**Commit**: B2 — `feat(backend): implement employee CRUD service — TDD (12 tests passing)`

---

## Sub-Agent Task Prompt

```
You are LOGIC, the Backend Engineer agent in the aGi squad.

Task: Implement the Employee CRUD service for a salary management system.

MANDATORY: Follow strict TDD — write ALL 12 failing tests first, then implement.

## Step 1 — RED (write ALL failing tests first)
Create `tests/test_employee_service.py` with these 12 test cases:

class TestCreateEmployee:
  - test_create_employee_returns_employee_with_id
  - test_create_employee_persists_all_fields
  - test_create_employee_with_duplicate_email_raises_conflict_error

class TestGetEmployee:
  - test_get_employee_by_id_returns_correct_employee
  - test_get_employee_by_id_raises_not_found_for_missing_id

class TestListEmployees:
  - test_list_employees_returns_paginated_results
  - test_list_employees_respects_page_and_page_size
  - test_list_employees_filters_by_country
  - test_list_employees_filters_by_job_title

class TestUpdateEmployee:
  - test_update_employee_returns_updated_values
  - test_update_nonexistent_employee_raises_not_found

class TestDeleteEmployee:
  - test_delete_employee_removes_from_database
  - test_delete_nonexistent_employee_raises_not_found

Run pytest — confirm all 12 FAIL before writing implementation.

## Step 2 — GREEN (implement employee_service.py)
Create `app/services/employee_service.py` with:
- create_employee(db, data: EmployeeCreate) -> Employee
- get_employee_by_id(db, employee_id: int) -> Employee
- list_employees(db, page, page_size, country, job_title, search) -> (list[Employee], total)
- update_employee(db, employee_id, data: EmployeeUpdate) -> Employee
- delete_employee(db, employee_id) -> None

Error handling:
- Raise HTTPException(404) when employee not found
- Raise HTTPException(409) when email already exists (unique constraint violation)

## Step 3 — REFACTOR
- Keep functions small and focused (single responsibility)
- No magic values — use named parameters
- Add docstrings to each function
- Run pytest — all 12 tests must pass

## Constraints
- Use db_session fixture from conftest.py (already created by ARCHIE)
- Tests must be deterministic (use fixed test data, not random)
- Test helper: create a reusable `make_employee_data()` factory function
- All functions must have full type annotations
```

---

## Key AI Decisions

1. **HTTPException in service layer** — debated whether errors belong in routes or services. Chose service layer for consistency — avoids duplicate error handling logic when multiple routes call the same service.
2. **Pagination as `(items, total)` tuple** — enables the router to return total count without a second query; total is computed with `COUNT(*)` in the same query using SQLAlchemy.
3. **`search` parameter on list** — searches across `full_name` using `ILIKE`-equivalent — adds HR usability beyond minimum requirements.
4. **Conflict detection** — catches `IntegrityError` from SQLAlchemy and re-raises as `HTTPException(409)` to avoid leaking DB internals.

## Test Results

```
12 passed in Xs
```
