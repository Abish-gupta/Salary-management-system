"""Tests for FastAPI endpoints — written BEFORE implementation.

TDD Phase: RED
These tests verify the RESTful API layer. They use FastAPI's TestClient
to simulate HTTP requests. Since the routers don't exist yet, these
requests will return 404 Not Found, failing the tests.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestEmployeeAPI:
    def test_create_employee_endpoint(self):
        """Should return 201 Created on success."""
        payload = {
            "full_name": "API Test User",
            "email": "api.test@example.com",
            "job_title": "Developer",
            "department": "Engineering",
            "country": "UK",
            "salary": 80000,
            "hire_date": "2023-05-10"
        }
        response = client.post("/api/employees", json=payload)
        
        # This will fail with 404 until we implement the router
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["email"] == payload["email"]

    def test_list_employees_endpoint(self):
        """Should return a paginated list of employees."""
        response = client.get("/api/employees?skip=0&limit=10")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)

    def test_get_employee_endpoint(self):
        """Should return a specific employee by ID."""
        # First create one
        payload = {
            "full_name": "Fetch Me",
            "email": "fetch.me@example.com",
            "job_title": "QA",
            "department": "Engineering",
            "country": "UK",
            "salary": 50000,
            "hire_date": "2023-01-01"
        }
        create_res = client.post("/api/employees", json=payload)
        # If create fails, the test stops here, which is expected in RED phase
        if create_res.status_code != 201:
            pytest.fail(f"Setup failed: {create_res.status_code}")
            
        emp_id = create_res.json()["id"]
        
        # Then fetch it
        response = client.get(f"/api/employees/{emp_id}")
        assert response.status_code == 200
        assert response.json()["full_name"] == "Fetch Me"

    def test_update_employee_endpoint(self):
        """Should return 200 OK after partial update."""
        # We need an ID to update. We'll try fetching ID 1 (assuming it might exist or test will fail gracefully)
        # A better pattern in TDD is creating one first, but we keep it simple here.
        payload = {
            "full_name": "Update Me",
            "email": "update.me@example.com",
            "job_title": "Intern",
            "department": "Engineering",
            "country": "UK",
            "salary": 30000,
            "hire_date": "2023-01-01"
        }
        create_res = client.post("/api/employees", json=payload)
        if create_res.status_code != 201:
            pytest.fail("Setup failed")
            
        emp_id = create_res.json()["id"]
        
        update_res = client.patch(f"/api/employees/{emp_id}", json={"salary": 45000})
        assert update_res.status_code == 200
        assert update_res.json()["salary"] == 45000

    def test_delete_employee_endpoint(self):
        """Should return 204 No Content on delete."""
        payload = {
            "full_name": "Delete Me",
            "email": "delete.me@example.com",
            "job_title": "Intern",
            "department": "Engineering",
            "country": "UK",
            "salary": 30000,
            "hire_date": "2023-01-01"
        }
        create_res = client.post("/api/employees", json=payload)
        if create_res.status_code != 201:
            pytest.fail("Setup failed")
            
        emp_id = create_res.json()["id"]
        
        delete_res = client.delete(f"/api/employees/{emp_id}")
        assert delete_res.status_code == 204


class TestAnalyticsAPI:
    def test_global_analytics_endpoint(self):
        """Should return 200 with global stats payload."""
        response = client.get("/api/analytics/global")
        assert response.status_code == 200
        
        data = response.json()
        assert "min_salary" in data
        assert "total_employees" in data

    def test_country_analytics_endpoint(self):
        """Should return 200 with list of country stats."""
        response = client.get("/api/analytics/country")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_department_analytics_endpoint(self):
        """Should return 200 with list of department stats."""
        response = client.get("/api/analytics/department")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
