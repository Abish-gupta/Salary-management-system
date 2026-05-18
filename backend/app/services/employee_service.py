"""Employee CRUD service logic.

This module encapsulates all database operations for Employee records.
It translates Pydantic schemas to SQLAlchemy models and handles
database exceptions, raising appropriate HTTPExceptions.
"""

from typing import Optional, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    """Create a new employee record.

    Raises:
        HTTPException(409) if the email is already in use.
    """
    employee = Employee(**data.model_dump())
    db.add(employee)

    try:
        db.commit()
        db.refresh(employee)
        return employee
    except IntegrityError as e:
        db.rollback()
        # SQLAlchemy throws IntegrityError when the UNIQUE constraint on email fails
        if "email" in str(e).lower() or "unique constraint" in str(e).lower():
            raise HTTPException(status_code=409, detail="Email already registered")
        raise HTTPException(status_code=400, detail="Database integrity error") from e


def get_employee_by_id(db: Session, employee_id: int) -> Employee:
    """Fetch an employee by their ID.

    Raises:
        HTTPException(404) if not found.
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


def list_employees(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    country: Optional[str] = None,
    job_title: Optional[str] = None,
    search: Optional[str] = None,
) -> Tuple[list[Employee], int]:
    """List employees with pagination, filtering, and searching.

    Returns:
        A tuple of (items, total_count).
    """
    query = db.query(Employee)

    # Apply filters
    if country:
        query = query.filter(Employee.country == country)

    if job_title:
        query = query.filter(Employee.job_title == job_title)

    if search:
        # Simple ILIKE search on full_name
        search_term = f"%{search}%"
        query = query.filter(Employee.full_name.ilike(search_term))

    # Get total count before pagination
    total = query.count()

    # Apply pagination and sorting (newest first)
    items = query.order_by(Employee.created_at.desc()).offset(skip).limit(limit).all()

    return items, total


def update_employee(db: Session, employee_id: int, data: EmployeeUpdate) -> Employee:
    """Partially update an employee.

    Raises:
        HTTPException(404) if not found.
        HTTPException(409) if changing to an email that is already taken.
    """
    employee = get_employee_by_id(db, employee_id)

    # Extract only the fields that were actually provided (not None)
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(employee, key, value)

    try:
        db.commit()
        db.refresh(employee)
        return employee
    except IntegrityError as e:
        db.rollback()
        if "email" in str(e).lower() or "unique constraint" in str(e).lower():
            raise HTTPException(status_code=409, detail="Email already registered")
        raise HTTPException(status_code=400, detail="Database integrity error") from e


def delete_employee(db: Session, employee_id: int) -> None:
    """Delete an employee by ID.

    Raises:
        HTTPException(404) if not found.
    """
    employee = get_employee_by_id(db, employee_id)
    db.delete(employee)
    db.commit()
