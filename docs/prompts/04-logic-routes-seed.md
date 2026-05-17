# Prompt 04 — LOGIC: API Routes + Seed Script (Commit B4)

**Date**: 2026-05-17  
**Agent**: LOGIC (Backend Engineer)  
**Branch**: `feature/backend`  
**Commit**: B4 — `feat(backend): add API routes, seed script with performance test — TDD`

---

## Sub-Agent Task Prompt

```
You are LOGIC, the Backend Engineer agent in the aGi squad.

Task: Wire FastAPI routes and create the performant 10K seed script.

MANDATORY: TDD — write failing tests first for routes, then implement.

## Step 1 — RED (write failing tests)

### tests/test_employee_router.py (10 tests):
class TestEmployeeRoutes:
  - test_create_employee_returns_201_with_body
  - test_create_employee_with_invalid_data_returns_422
  - test_get_employee_returns_200_with_correct_data
  - test_get_nonexistent_employee_returns_404
  - test_list_employees_returns_paginated_response
  - test_list_employees_filter_by_country
  - test_update_employee_returns_200_with_new_values
  - test_update_nonexistent_employee_returns_404
  - test_delete_employee_returns_204
  - test_delete_nonexistent_employee_returns_404

### tests/test_analytics_router.py (4 tests):
  - test_country_stats_returns_200_for_valid_country
  - test_all_country_stats_returns_list
  - test_job_title_stats_by_country_returns_200
  - test_top_earners_returns_correct_count

### tests/test_seed.py (2 tests):
  - test_seed_inserts_correct_count (10,000 employees)
  - test_seed_performance_under_threshold (must complete in < 5 seconds)

## Step 2 — GREEN (implement)

### app/routers/employees.py
Endpoints:
  GET    /api/employees          (list with ?page, ?page_size, ?country, ?job_title, ?search)
  POST   /api/employees          (create)
  GET    /api/employees/{id}     (get by id)
  PUT    /api/employees/{id}     (full update)
  DELETE /api/employees/{id}     (delete, returns 204)

### app/routers/analytics.py
Endpoints:
  GET /api/analytics/countries              (all country stats)
  GET /api/analytics/countries/{country}    (single country stats)
  GET /api/analytics/countries/{country}/job-titles  (job title breakdown)
  GET /api/analytics/top-earners            (top 10, ?limit param)
  GET /api/analytics/departments            (department distribution)

### app/seed/first_names.txt + last_names.txt
Generate 200+ realistic first names and 200+ last names.
Cover diverse global names (Indian, British, American, European, African, East Asian).

### app/seed/seed.py
Algorithm:
  1. Read first_names.txt and last_names.txt into memory
  2. Generate 10,000 employee dicts (list comprehension, not loop)
  3. Use engine.begin() + conn.execute(insert(Employee), list_of_dicts)
  4. Single transaction — atomic, fast
  5. Target: < 3 seconds for 10,000 rows

CLI: python -m app.seed.seed [--count N] [--clear]
  --count: number of employees (default 10000)
  --clear: drop existing employees before seeding

### app/main.py
Wire both routers:
  app.include_router(employee_router, prefix="/api")
  app.include_router(analytics_router, prefix="/api")

## Step 3 — REFACTOR
- Router files should be thin — just HTTP concerns, delegate to services
- Add proper response_model and status_code to all decorators
- No business logic in route handlers
- Run pytest — all 16 tests must pass

## Constraints
- Seed uses bulk insert NOT session.add() in a loop
- Names from files must be combined: random.choice(first_names) + " " + random.choice(last_names)
- Seed must be idempotent when --clear flag is used
- Type annotations on all route handlers
```

---

## Key AI Decisions

1. **`engine.begin()` for bulk insert** — bypasses ORM completely for maximum insert throughput. Assessment says performance matters.
2. **`--clear` flag on seed** — assessment says "engineers run this regularly". Clear + reseed is a common pattern in dev/staging environments.
3. **204 on DELETE** — semantically correct: no content to return after deletion. 200 with a message would also be acceptable but 204 is the REST standard.
4. **Diverse name files** — covering Indian, British, American, African, East Asian names makes the seeded data realistic for a global org analytics demo.

## Test Results

```
16 route tests + 2 seed tests = 18 passed in Xs
```
