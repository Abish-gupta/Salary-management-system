# Prompt 03 — LOGIC: Analytics Service (Commit B3)

**Date**: 2026-05-17  
**Agent**: LOGIC (Backend Engineer)  
**Branch**: `feature/backend`  
**Commit**: B3 — `feat(backend): implement salary analytics service — TDD (8 tests passing)`

---

## Sub-Agent Task Prompt

```
You are LOGIC, the Backend Engineer agent in the aGi squad.

Task: Implement the Salary Analytics service for a salary management system.

MANDATORY: Follow strict TDD — write ALL failing tests first, then implement.

## Step 1 — RED (write ALL failing tests first)
Create `tests/test_analytics_service.py` with these 8 test cases:

class TestCountryStats:
  - test_country_stats_returns_min_max_avg_count_for_country
  - test_country_stats_for_nonexistent_country_returns_zeros
  - test_all_country_stats_groups_all_employees_correctly

class TestJobTitleStats:
  - test_job_title_avg_salary_in_country
  - test_job_title_stats_excludes_other_countries
  - test_job_title_stats_returns_employee_count_per_role

class TestAdditionalMetrics:
  - test_top_earners_returns_n_employees_sorted_desc
  - test_department_distribution_returns_headcount_per_department

Seed 5-6 deterministic employees in each test (no random data).
Run pytest — confirm all 8 FAIL before writing implementation.

## Step 2 — GREEN (implement analytics_service.py)
Create `app/services/analytics_service.py` with:

- get_country_stats(db, country: str) -> CountrySalaryStats
  Returns: min, max, avg salary + employee count for a country

- get_all_country_stats(db) -> list[CountrySalaryStats]
  Returns stats grouped by all countries

- get_job_title_stats_by_country(db, country: str) -> list[JobTitleStats]
  Returns avg salary + count per job title within a country

- get_top_earners(db, limit: int = 10) -> list[Employee]
  Returns top N employees by salary (descending)

- get_department_distribution(db) -> list[DepartmentStats]
  Returns employee count per department

Create response models in `app/schemas/analytics.py`:
- CountrySalaryStats: country, min_salary, max_salary, avg_salary, employee_count, total_payroll
- JobTitleStats: job_title, avg_salary, employee_count, min_salary, max_salary
- DepartmentStats: department, employee_count

## Step 3 — REFACTOR
- All queries must use SQLAlchemy (no raw SQL strings)
- Use func.min(), func.max(), func.avg(), func.count() 
- Group by queries must use .group_by()
- Results ordered consistently (by country name, by salary desc, etc.)
- Run pytest — all 8 tests must pass

## Constraints
- No N+1 queries — analytics must be single SQL queries with GROUP BY
- Round avg_salary to 2 decimal places in the response schema
- All functions fully typed
```

---

## Key AI Decisions

1. **SQLAlchemy `func` aggregates** — avoids raw SQL strings, keeps queries composable and ORM-friendly
2. **Separate `analytics.py` schema file** — analytics response shapes are different from employee CRUD shapes; keeping them separate avoids a bloated single schema file
3. **`total_payroll` as bonus metric** — useful for HR budget planning; costs nothing since SUM is trivially added to the same GROUP BY query
4. **Median not included** — SQLite doesn't have a native MEDIAN aggregate. Including it would require a complex subquery or Python post-processing. Documented as a limitation in tradeoffs.md.

## Test Results

```
8 passed in Xs
```
