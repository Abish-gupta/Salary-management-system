"""High-performance database seeder for the Salary Management System.

This script generates 10,000 random employee records and inserts them
into the database using SQLAlchemy bulk inserts for maximum performance.
"""

import sys
import os
import random
import time
from datetime import datetime, timedelta

# Add backend directory to sys.path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import insert
from app.database import engine, SessionLocal, create_tables
from app.models.employee import Employee


# Seed Data Pools
FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley", "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle", "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "David", "George", "Melissa", "Timothy", "Deborah"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts"]
DEPARTMENTS = ["Engineering", "Product", "Sales", "Marketing", "HR", "Finance", "Customer Support", "Legal", "Operations", "Design"]
TITLES = ["Junior", "Mid-Level", "Senior", "Lead", "Principal", "Manager", "Director", "VP"]
COUNTRIES = ["USA", "UK", "Canada", "Australia", "India", "Germany", "France", "Japan", "Brazil", "Singapore"]


def generate_random_date(start_year=2015, end_year=2024):
    """Generate a random hire date."""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return (start_date + timedelta(days=random_number_of_days)).date()


def generate_salary(department, title_level):
    """Generate a realistic salary based on department and seniority."""
    base = {
        "Engineering": 80000,
        "Product": 75000,
        "Sales": 50000,
        "Marketing": 60000,
        "HR": 55000,
        "Finance": 70000,
        "Customer Support": 45000,
        "Legal": 90000,
        "Operations": 65000,
        "Design": 70000
    }.get(department, 60000)
    
    multiplier = {
        "Junior": 0.8,
        "Mid-Level": 1.0,
        "Senior": 1.3,
        "Lead": 1.5,
        "Principal": 1.8,
        "Manager": 1.6,
        "Director": 2.0,
        "VP": 2.5
    }.get(title_level, 1.0)
    
    # Add randomness (+/- 10%)
    variation = random.uniform(0.9, 1.1)
    return round(base * multiplier * variation, 2)


def seed_database(num_records=10000):
    """Generate and insert employee records."""
    print(f"Ensuring database tables exist...")
    create_tables()

    print(f"Generating {num_records} employee records...")
    start_time = time.time()
    
    employees_data = []
    
    for i in range(num_records):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        department = random.choice(DEPARTMENTS)
        title_level = random.choice(TITLES)
        
        job_title = f"{title_level} {department.rstrip('s')} Specialist"
        if department == "Engineering":
            job_title = f"{title_level} Software Engineer"
            
        salary = generate_salary(department, title_level)
        
        # Format the email logically
        email = f"{first_name.lower()}.{last_name.lower()}.{i}@incubyte.example.com"
        
        employees_data.append({
            "full_name": f"{first_name} {last_name}",
            "email": email,
            "job_title": job_title,
            "department": department,
            "country": random.choice(COUNTRIES),
            "salary": salary,
            "hire_date": generate_random_date()
        })
        
    generation_time = time.time() - start_time
    print(f"Generation completed in {generation_time:.2f} seconds.")
    
    print(f"Bulk inserting records into the database...")
    insert_start = time.time()
    
    db = SessionLocal()
    try:
        # Check if we already have data
        existing = db.query(Employee).count()
        if existing >= num_records:
            print(f"Database already has {existing} records. Skipping seed.")
            return

        # Perform bulk insert
        db.execute(insert(Employee), employees_data)
        db.commit()
        
        insert_time = time.time() - insert_start
        print(f"Successfully inserted {num_records} records in {insert_time:.2f} seconds!")
        print(f"Total time: {generation_time + insert_time:.2f} seconds.")
        
    except Exception as e:
        db.rollback()
        print(f"Error during bulk insert: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    count = 10000
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print("Invalid number of records provided. Defaulting to 10000.")
            
    seed_database(count)
