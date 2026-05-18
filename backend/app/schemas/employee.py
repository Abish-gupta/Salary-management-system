"""Pydantic schemas for Employee request validation and response serialization.

Three schemas with a clear purpose each:
- EmployeeCreate  : Validates incoming POST /employees body
- EmployeeUpdate  : Validates PATCH /employees/{id} body (all fields optional)
- EmployeeResponse: Shapes the JSON response (includes DB-generated fields)

Design decisions:
- Pydantic v2 used throughout (model_config, model_dump)
- salary validated as > 0 at the schema level (belt-and-suspenders with DB constraint)
- full_name stripped and length-validated to catch empty-string inputs
- EmployeeUpdate uses Optional[...] = None for all fields (partial update pattern)
- from_attributes=True on response enables constructing from SQLAlchemy ORM objects
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class EmployeeCreate(BaseModel):
    """Schema for creating a new employee.

    All fields are required except currency (defaults to USD).
    """

    full_name: str = Field(
        ..., min_length=1, max_length=200, description="Employee's full name"
    )
    email: EmailStr = Field(..., description="Unique work email address")
    job_title: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    salary: Decimal = Field(
        ..., gt=0, description="Annual salary — must be greater than zero"
    )
    currency: str = Field(
        default="USD", min_length=3, max_length=3, description="ISO 4217 currency code"
    )
    hire_date: date = Field(..., description="Date when the employee joined")

    @field_validator("full_name", mode="before")
    @classmethod
    def strip_full_name(cls, v: str) -> str:
        """Strip leading/trailing whitespace. Reject after stripping if empty."""
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                raise ValueError("full_name cannot be blank")
            return stripped
        return v

    @field_validator("currency", mode="before")
    @classmethod
    def uppercase_currency(cls, v: str) -> str:
        """Normalize currency code to uppercase (e.g. 'usd' → 'USD')."""
        if isinstance(v, str):
            return v.upper()
        return v


class EmployeeUpdate(BaseModel):
    """Schema for partially updating an employee.

    All fields are optional — send only what needs to change.
    """

    full_name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    job_title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    department: Optional[str] = Field(default=None, min_length=1, max_length=100)
    country: Optional[str] = Field(default=None, min_length=1, max_length=100)
    salary: Optional[Decimal] = Field(default=None, gt=0)
    currency: Optional[str] = Field(default=None, min_length=3, max_length=3)
    hire_date: Optional[date] = None

    @field_validator("currency", mode="before")
    @classmethod
    def uppercase_currency(cls, v: Optional[str]) -> Optional[str]:
        """Normalize currency code to uppercase."""
        if isinstance(v, str):
            return v.upper()
        return v


class EmployeeResponse(BaseModel):
    """Schema for serializing an employee record in API responses.

    Includes all fields from the database row, including auto-generated ones.
    `from_attributes=True` allows Pydantic to read from SQLAlchemy ORM objects.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    job_title: str
    department: str
    country: str
    salary: Decimal
    currency: str
    hire_date: date
    created_at: datetime
    updated_at: datetime


class PaginatedEmployeeResponse(BaseModel):
    """Paginated list of employees with metadata."""

    items: list[EmployeeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
