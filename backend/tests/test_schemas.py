"""Tests for Pydantic schemas — written BEFORE the schema implementation.

TDD Phase: RED — all tests will fail until schemas are implemented.

These tests verify that:
- Required fields are enforced
- Invalid data is rejected with clear errors
- Optional fields have correct defaults
- Response schema includes computed/auto fields
"""

import pytest
from datetime import date
from pydantic import ValidationError


# ── EmployeeCreate schema tests ────────────────────────────────────────────────

class TestEmployeeCreateSchema:
    """Tests for the EmployeeCreate request schema."""

    def test_valid_employee_create_passes_validation(self):
        """A fully valid payload should deserialize without errors."""
        from app.schemas.employee import EmployeeCreate

        employee = EmployeeCreate(
            full_name="Jane Doe",
            email="jane.doe@example.com",
            job_title="Software Engineer",
            department="Engineering",
            country="India",
            salary=120000.00,
            hire_date=date(2022, 3, 15),
        )
        assert employee.full_name == "Jane Doe"
        assert employee.salary == 120000.00
        assert employee.currency == "USD"  # default value

    def test_full_name_is_required(self):
        """Missing full_name should raise a ValidationError."""
        from app.schemas.employee import EmployeeCreate

        with pytest.raises(ValidationError) as exc_info:
            EmployeeCreate(
                email="test@example.com",
                job_title="Engineer",
                department="Engineering",
                country="India",
                salary=100000,
                hire_date=date(2022, 1, 1),
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("full_name",) for e in errors)

    def test_email_is_required(self):
        """Missing email should raise a ValidationError."""
        from app.schemas.employee import EmployeeCreate

        with pytest.raises(ValidationError):
            EmployeeCreate(
                full_name="Jane Doe",
                job_title="Engineer",
                department="Engineering",
                country="India",
                salary=100000,
                hire_date=date(2022, 1, 1),
            )

    def test_negative_salary_is_rejected(self):
        """Salary must be a positive number."""
        from app.schemas.employee import EmployeeCreate

        with pytest.raises(ValidationError) as exc_info:
            EmployeeCreate(
                full_name="Jane Doe",
                email="jane@example.com",
                job_title="Engineer",
                department="Engineering",
                country="India",
                salary=-5000,
                hire_date=date(2022, 1, 1),
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("salary",) for e in errors)

    def test_zero_salary_is_rejected(self):
        """Salary must be greater than zero."""
        from app.schemas.employee import EmployeeCreate

        with pytest.raises(ValidationError):
            EmployeeCreate(
                full_name="Jane Doe",
                email="jane@example.com",
                job_title="Engineer",
                department="Engineering",
                country="India",
                salary=0,
                hire_date=date(2022, 1, 1),
            )

    def test_currency_defaults_to_usd(self):
        """Currency should default to USD when not provided."""
        from app.schemas.employee import EmployeeCreate

        employee = EmployeeCreate(
            full_name="John Smith",
            email="john@example.com",
            job_title="Manager",
            department="HR",
            country="USA",
            salary=95000,
            hire_date=date(2021, 6, 1),
        )
        assert employee.currency == "USD"

    def test_full_name_cannot_be_empty_string(self):
        """An empty string for full_name should be rejected."""
        from app.schemas.employee import EmployeeCreate

        with pytest.raises(ValidationError):
            EmployeeCreate(
                full_name="",
                email="test@example.com",
                job_title="Engineer",
                department="Engineering",
                country="India",
                salary=100000,
                hire_date=date(2022, 1, 1),
            )

    def test_country_is_required(self):
        """Missing country should raise a ValidationError."""
        from app.schemas.employee import EmployeeCreate

        with pytest.raises(ValidationError):
            EmployeeCreate(
                full_name="Jane Doe",
                email="jane@example.com",
                job_title="Engineer",
                department="Engineering",
                salary=100000,
                hire_date=date(2022, 1, 1),
            )


# ── EmployeeUpdate schema tests ────────────────────────────────────────────────

class TestEmployeeUpdateSchema:
    """Tests for the EmployeeUpdate schema (all fields optional)."""

    def test_employee_update_all_fields_optional(self):
        """EmployeeUpdate should accept an empty payload (partial update)."""
        from app.schemas.employee import EmployeeUpdate

        update = EmployeeUpdate()
        assert update.salary is None
        assert update.job_title is None

    def test_employee_update_partial_salary(self):
        """Should allow updating only the salary."""
        from app.schemas.employee import EmployeeUpdate

        update = EmployeeUpdate(salary=150000)
        assert update.salary == 150000

    def test_employee_update_rejects_negative_salary(self):
        """Even on update, salary must be positive."""
        from app.schemas.employee import EmployeeUpdate

        with pytest.raises(ValidationError):
            EmployeeUpdate(salary=-1000)


# ── EmployeeResponse schema tests ──────────────────────────────────────────────

class TestEmployeeResponseSchema:
    """Tests for the EmployeeResponse output schema."""

    def test_employee_response_includes_id(self):
        """Response schema must include the database-generated id."""
        from app.schemas.employee import EmployeeResponse
        from datetime import datetime

        response = EmployeeResponse(
            id=1,
            full_name="Jane Doe",
            email="jane@example.com",
            job_title="Engineer",
            department="Engineering",
            country="India",
            salary=120000,
            currency="USD",
            hire_date=date(2022, 1, 1),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        assert response.id == 1

    def test_employee_response_serializes_to_dict(self):
        """Response schema should serialize cleanly to a dict."""
        from app.schemas.employee import EmployeeResponse
        from datetime import datetime

        response = EmployeeResponse(
            id=42,
            full_name="Bob",
            email="bob@example.com",
            job_title="Analyst",
            department="Finance",
            country="UK",
            salary=80000,
            currency="GBP",
            hire_date=date(2020, 5, 10),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        data = response.model_dump()
        assert data["id"] == 42
        assert data["full_name"] == "Bob"
