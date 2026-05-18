"""Tests for the Employee CRUD service — written BEFORE implementation.

TDD Phase: RED — these tests will fail until app/services/employee_service.py is implemented.

These tests verify the core business logic for employee management:
- Creating employees (and handling email conflicts)
- Retrieving employees by ID (handling not found)
- Listing employees with pagination and filtering
- Updating employees
- Deleting employees
"""

import pytest
from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.employee import EmployeeCreate, EmployeeUpdate
# We will import the service once it's created
# from app.services import employee_service


# ── Test Data Factory ──────────────────────────────────────────────────────────

def make_employee_data(email: str = "test@example.com") -> EmployeeCreate:
    """Helper to generate valid employee creation data."""
    return EmployeeCreate(
        full_name="John Doe",
        email=email,
        job_title="Software Engineer",
        department="Engineering",
        country="USA",
        salary=100000.00,
        hire_date=date(2023, 1, 1),
    )


# ── Create Employee Tests ──────────────────────────────────────────────────────

class TestCreateEmployee:
    
    def test_create_employee_returns_employee_with_id(self, db_session: Session):
        """Creating an employee should persist to DB and return the object with an ID."""
        from app.services import employee_service
        
        data = make_employee_data()
        employee = employee_service.create_employee(db_session, data)
        
        assert employee.id is not None
        assert employee.email == data.email
        assert employee.full_name == data.full_name
        
    def test_create_employee_with_duplicate_email_raises_conflict_error(self, db_session: Session):
        """Creating an employee with an existing email should raise a 409 Conflict."""
        from app.services import employee_service
        
        data = make_employee_data(email="duplicate@example.com")
        employee_service.create_employee(db_session, data)
        
        with pytest.raises(HTTPException) as exc_info:
            employee_service.create_employee(db_session, data)
            
        assert exc_info.value.status_code == 409
        assert "Email already registered" in exc_info.value.detail


# ── Get Employee Tests ─────────────────────────────────────────────────────────

class TestGetEmployee:

    def test_get_employee_by_id_returns_correct_employee(self, db_session: Session):
        """Fetching by ID should return the exact employee."""
        from app.services import employee_service
        
        created = employee_service.create_employee(db_session, make_employee_data())
        fetched = employee_service.get_employee_by_id(db_session, created.id)
        
        assert fetched is not None
        assert fetched.id == created.id
        
    def test_get_employee_by_id_raises_not_found_for_missing_id(self, db_session: Session):
        """Fetching a non-existent ID should raise a 404 Not Found."""
        from app.services import employee_service
        
        with pytest.raises(HTTPException) as exc_info:
            employee_service.get_employee_by_id(db_session, 99999)
            
        assert exc_info.value.status_code == 404


# ── List Employees Tests ───────────────────────────────────────────────────────

class TestListEmployees:

    @pytest.fixture
    def seed_employees(self, db_session: Session):
        """Seed a few employees for list tests."""
        from app.services import employee_service
        
        e1 = make_employee_data(email="1@test.com")
        e1.country = "USA"
        e1.job_title = "Engineer"
        e1.full_name = "Alice Smith"
        
        e2 = make_employee_data(email="2@test.com")
        e2.country = "India"
        e2.job_title = "Manager"
        e2.full_name = "Bob Jones"
        
        e3 = make_employee_data(email="3@test.com")
        e3.country = "USA"
        e3.job_title = "Manager"
        e3.full_name = "Charlie Brown"
        
        employee_service.create_employee(db_session, e1)
        employee_service.create_employee(db_session, e2)
        employee_service.create_employee(db_session, e3)

    def test_list_employees_returns_paginated_results(self, db_session: Session, seed_employees):
        """List should return items and a total count."""
        from app.services import employee_service
        
        items, total = employee_service.list_employees(db_session, skip=0, limit=10)
        assert total == 3
        assert len(items) == 3

    def test_list_employees_respects_skip_and_limit(self, db_session: Session, seed_employees):
        """Pagination logic should work correctly."""
        from app.services import employee_service
        
        items, total = employee_service.list_employees(db_session, skip=1, limit=1)
        assert total == 3
        assert len(items) == 1

    def test_list_employees_filters_by_country(self, db_session: Session, seed_employees):
        """Should filter exact matches on country."""
        from app.services import employee_service
        
        items, total = employee_service.list_employees(db_session, skip=0, limit=10, country="USA")
        assert total == 2
        assert all(i.country == "USA" for i in items)

    def test_list_employees_filters_by_job_title(self, db_session: Session, seed_employees):
        """Should filter exact matches on job title."""
        from app.services import employee_service
        
        items, total = employee_service.list_employees(db_session, skip=0, limit=10, job_title="Manager")
        assert total == 2
        assert all(i.job_title == "Manager" for i in items)
        
    def test_list_employees_search_by_name(self, db_session: Session, seed_employees):
        """Should perform ILIKE search on full_name."""
        from app.services import employee_service
        
        items, total = employee_service.list_employees(db_session, skip=0, limit=10, search="alice")
        assert total == 1
        assert items[0].full_name == "Alice Smith"


# ── Update Employee Tests ──────────────────────────────────────────────────────

class TestUpdateEmployee:

    def test_update_employee_returns_updated_values(self, db_session: Session):
        """Updating an employee should save changes and return the new state."""
        from app.services import employee_service
        
        created = employee_service.create_employee(db_session, make_employee_data())
        
        update_data = EmployeeUpdate(salary=150000.00, job_title="Senior Engineer")
        updated = employee_service.update_employee(db_session, created.id, update_data)
        
        assert updated.salary == 150000.00
        assert updated.job_title == "Senior Engineer"
        # Untouched fields remain the same
        assert updated.email == created.email

    def test_update_nonexistent_employee_raises_not_found(self, db_session: Session):
        """Updating a missing employee should raise 404."""
        from app.services import employee_service
        
        with pytest.raises(HTTPException) as exc_info:
            employee_service.update_employee(db_session, 99999, EmployeeUpdate(salary=1))
        assert exc_info.value.status_code == 404


# ── Delete Employee Tests ──────────────────────────────────────────────────────

class TestDeleteEmployee:

    def test_delete_employee_removes_from_database(self, db_session: Session):
        """Deleting an employee should remove them entirely."""
        from app.services import employee_service
        
        created = employee_service.create_employee(db_session, make_employee_data())
        
        employee_service.delete_employee(db_session, created.id)
        
        with pytest.raises(HTTPException) as exc_info:
            employee_service.get_employee_by_id(db_session, created.id)
        assert exc_info.value.status_code == 404

    def test_delete_nonexistent_employee_raises_not_found(self, db_session: Session):
        """Deleting a missing employee should raise 404."""
        from app.services import employee_service
        
        with pytest.raises(HTTPException) as exc_info:
            employee_service.delete_employee(db_session, 99999)
        assert exc_info.value.status_code == 404
