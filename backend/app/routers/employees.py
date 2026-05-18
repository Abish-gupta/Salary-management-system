"""API Endpoints for Employee CRUD operations."""

from typing import Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, PaginatedEmployeeResponse
from app.services import employee_service

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: EmployeeCreate, 
    db: Session = Depends(get_db)
) -> Any:
    """Create a new employee."""
    return employee_service.create_employee(db, employee)


@router.get("", response_model=PaginatedEmployeeResponse)
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    country: str | None = None,
    job_title: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
) -> Any:
    """Retrieve a paginated list of employees with optional filtering."""
    items, total = employee_service.list_employees(
        db, skip=skip, limit=limit, country=country, job_title=job_title, search=search
    )
    return {
        "items": items, 
        "total": total,
        "page": (skip // limit) + 1,
        "page_size": limit,
        "total_pages": (total + limit - 1) // limit
    }


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int, 
    db: Session = Depends(get_db)
) -> Any:
    """Retrieve a specific employee by ID."""
    return employee_service.get_employee_by_id(db, employee_id)


@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int, 
    employee: EmployeeUpdate, 
    db: Session = Depends(get_db)
) -> Any:
    """Partially update an employee."""
    return employee_service.update_employee(db, employee_id, employee)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int, 
    db: Session = Depends(get_db)
) -> None:
    """Delete an employee."""
    employee_service.delete_employee(db, employee_id)
