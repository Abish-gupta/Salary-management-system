"""API Endpoints for Salary Analytics."""

from typing import Any, List, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import analytics_service

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/global", response_model=Dict[str, Any])
def get_global_analytics(db: Session = Depends(get_db)) -> Any:
    """Retrieve overall salary statistics."""
    return analytics_service.get_global_salary_stats(db)


@router.get("/country", response_model=List[Dict[str, Any]])
def get_country_analytics(db: Session = Depends(get_db)) -> Any:
    """Retrieve salary statistics grouped by country."""
    return analytics_service.get_salary_stats_by_country(db)


@router.get("/department", response_model=List[Dict[str, Any]])
def get_department_analytics(db: Session = Depends(get_db)) -> Any:
    """Retrieve salary statistics grouped by department."""
    return analytics_service.get_salary_stats_by_department(db)
