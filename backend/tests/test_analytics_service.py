"""Tests for the Analytics Service — written BEFORE implementation.

TDD Phase: RED
These tests verify that we can aggregate salary data accurately:
- Global min, max, and average salary.
- Aggregations grouped by country.
- Aggregations grouped by department.
"""

import pytest
from sqlalchemy.orm import Session
from decimal import Decimal

from app.schemas.employee import EmployeeCreate


@pytest.fixture
def seed_analytics_data(db_session: Session):
    """Seed data to test aggregation and grouping logic."""
    from app.services import employee_service

    employees = [
        # USA Engineering
        EmployeeCreate(
            full_name="USA Eng 1", email="u.e1@test.com", 
            job_title="Engineer", department="Engineering", 
            country="USA", salary=100000.0, hire_date="2023-01-01"
        ),
        EmployeeCreate(
            full_name="USA Eng 2", email="u.e2@test.com", 
            job_title="Senior Engineer", department="Engineering", 
            country="USA", salary=150000.0, hire_date="2023-01-01"
        ),
        # USA HR
        EmployeeCreate(
            full_name="USA HR 1", email="u.h1@test.com", 
            job_title="HR Manager", department="HR", 
            country="USA", salary=90000.0, hire_date="2023-01-01"
        ),
        # India Engineering
        EmployeeCreate(
            full_name="IND Eng 1", email="i.e1@test.com", 
            job_title="Engineer", department="Engineering", 
            country="India", salary=40000.0, hire_date="2023-01-01"
        ),
        EmployeeCreate(
            full_name="IND Eng 2", email="i.e2@test.com", 
            job_title="Lead Engineer", department="Engineering", 
            country="India", salary=60000.0, hire_date="2023-01-01"
        )
    ]
    
    for emp in employees:
        employee_service.create_employee(db_session, emp)


class TestGlobalAnalytics:
    def test_global_salary_stats(self, db_session: Session, seed_analytics_data):
        """Should calculate overall min, max, and average salary correctly."""
        from app.services import analytics_service
        
        stats = analytics_service.get_global_salary_stats(db_session)
        
        # Expected:
        # Salaries: 100k, 150k, 90k, 40k, 60k
        # Min: 40,000 | Max: 150,000 | Avg: 440,000 / 5 = 88,000
        
        assert stats["min_salary"] == 40000.0
        assert stats["max_salary"] == 150000.0
        assert stats["avg_salary"] == 88000.0
        assert stats["total_employees"] == 5

    def test_global_salary_stats_empty_db(self, db_session: Session):
        """Should handle an empty database gracefully (return 0 or None)."""
        from app.services import analytics_service
        
        stats = analytics_service.get_global_salary_stats(db_session)
        
        assert stats["total_employees"] == 0
        assert stats["min_salary"] == 0.0
        assert stats["max_salary"] == 0.0
        assert stats["avg_salary"] == 0.0


class TestGroupedAnalytics:
    def test_salary_stats_by_country(self, db_session: Session, seed_analytics_data):
        """Should group analytics by country correctly."""
        from app.services import analytics_service
        
        stats = analytics_service.get_salary_stats_by_country(db_session)
        
        # We expect a dictionary-like structure keyed by country
        # USA: 100k, 150k, 90k -> Min 90k, Max 150k, Avg 113.33k
        # India: 40k, 60k -> Min 40k, Max 60k, Avg 50k
        
        usa_stats = next(s for s in stats if s["country"] == "USA")
        ind_stats = next(s for s in stats if s["country"] == "India")
        
        assert usa_stats["total_employees"] == 3
        assert usa_stats["min_salary"] == 90000.0
        assert usa_stats["max_salary"] == 150000.0
        assert round(usa_stats["avg_salary"], 2) == 113333.33
        
        assert ind_stats["total_employees"] == 2
        assert ind_stats["min_salary"] == 40000.0
        assert ind_stats["max_salary"] == 60000.0
        assert ind_stats["avg_salary"] == 50000.0

    def test_salary_stats_by_department(self, db_session: Session, seed_analytics_data):
        """Should group analytics by department correctly."""
        from app.services import analytics_service
        
        stats = analytics_service.get_salary_stats_by_department(db_session)
        
        # Engineering: 100k, 150k, 40k, 60k -> Min 40k, Max 150k, Avg 87.5k
        # HR: 90k -> Min 90k, Max 90k, Avg 90k
        
        eng_stats = next(s for s in stats if s["department"] == "Engineering")
        hr_stats = next(s for s in stats if s["department"] == "HR")
        
        assert eng_stats["total_employees"] == 4
        assert eng_stats["min_salary"] == 40000.0
        assert eng_stats["max_salary"] == 150000.0
        assert eng_stats["avg_salary"] == 87500.0
        
        assert hr_stats["total_employees"] == 1
        assert hr_stats["min_salary"] == 90000.0
        assert hr_stats["max_salary"] == 90000.0
        assert hr_stats["avg_salary"] == 90000.0
