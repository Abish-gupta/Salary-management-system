"""Analytics service for calculating salary statistics.

This module uses SQLAlchemy aggregation functions to compute
global and grouped salary statistics across the Employee database.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.employee import Employee


def get_global_salary_stats(db: Session) -> Dict[str, Any]:
    """Calculate overall min, max, and average salary for all employees."""
    result = db.query(
        func.count(Employee.id).label("total_employees"),
        func.min(Employee.salary).label("min_salary"),
        func.max(Employee.salary).label("max_salary"),
        func.avg(Employee.salary).label("avg_salary")
    ).first()
    
    # Handle the empty database case
    total = result.total_employees if result and result.total_employees else 0
    
    return {
        "total_employees": total,
        "min_salary": float(result.min_salary) if total > 0 else 0.0,
        "max_salary": float(result.max_salary) if total > 0 else 0.0,
        "avg_salary": float(result.avg_salary) if total > 0 else 0.0,
    }


def get_salary_stats_by_country(db: Session) -> List[Dict[str, Any]]:
    """Calculate salary statistics grouped by country."""
    results = db.query(
        Employee.country,
        func.count(Employee.id).label("total_employees"),
        func.min(Employee.salary).label("min_salary"),
        func.max(Employee.salary).label("max_salary"),
        func.avg(Employee.salary).label("avg_salary")
    ).group_by(Employee.country).all()
    
    return [
        {
            "country": row.country,
            "total_employees": row.total_employees,
            "min_salary": float(row.min_salary),
            "max_salary": float(row.max_salary),
            "avg_salary": float(row.avg_salary)
        }
        for row in results
    ]


def get_salary_stats_by_department(db: Session) -> List[Dict[str, Any]]:
    """Calculate salary statistics grouped by department."""
    results = db.query(
        Employee.department,
        func.count(Employee.id).label("total_employees"),
        func.min(Employee.salary).label("min_salary"),
        func.max(Employee.salary).label("max_salary"),
        func.avg(Employee.salary).label("avg_salary")
    ).group_by(Employee.department).all()
    
    return [
        {
            "department": row.department,
            "total_employees": row.total_employees,
            "min_salary": float(row.min_salary),
            "max_salary": float(row.max_salary),
            "avg_salary": float(row.avg_salary)
        }
        for row in results
    ]


def get_specific_country_stats(db: Session, country: str) -> Dict[str, Any]:
    """Calculate min, max, average salary and job title averages for a specific country."""
    # Overall country stats
    country_stats = db.query(
        func.count(Employee.id).label("total_employees"),
        func.min(Employee.salary).label("min_salary"),
        func.max(Employee.salary).label("max_salary"),
        func.avg(Employee.salary).label("avg_salary")
    ).filter(func.lower(Employee.country) == country.lower()).first()

    total = country_stats.total_employees if country_stats and country_stats.total_employees else 0

    # Job title stats within this country
    job_stats = db.query(
        Employee.job_title,
        func.avg(Employee.salary).label("avg_salary")
    ).filter(func.lower(Employee.country) == country.lower()).group_by(Employee.job_title).all()

    return {
        "country": country,
        "total_employees": total,
        "min_salary": float(country_stats.min_salary) if total > 0 else 0.0,
        "max_salary": float(country_stats.max_salary) if total > 0 else 0.0,
        "avg_salary": float(country_stats.avg_salary) if total > 0 else 0.0,
        "job_titles": [
            {
                "job_title": row.job_title,
                "avg_salary": float(row.avg_salary)
            }
            for row in job_stats
        ]
    }
