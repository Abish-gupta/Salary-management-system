"""Employee SQLAlchemy ORM model.

Design decisions:
- Surrogate integer PK (auto-increment) — avoids exposing business keys externally
- email UNIQUE constraint — prevents duplicates at the DB level, not just the app layer
- Indexed columns: country, job_title, (country, job_title) composite
  These three indexes serve the primary analytics query patterns
- salary stored as Numeric(12, 2) — precise decimal arithmetic, avoids float rounding
- hire_date as Date (not DateTime) — day-level precision is what HR needs
- created_at / updated_at for audit trail — auto-set on insert, auto-updated on change
"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Index,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Employee(Base):
    """Represents a single employee record in the organization.

    All analytics queries (country stats, job-title stats) filter on the
    indexed columns: country, job_title, and the composite index.
    """

    __tablename__ = "employees"

    # ── Primary key ────────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # ── Core fields (required by assessment) ──────────────────────────────────
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    job_title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    salary: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    # ── Additional meaningful fields ───────────────────────────────────────────
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)

    # ── Audit fields ───────────────────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # ── Table-level constraints and indexes ────────────────────────────────────
    __table_args__ = (
        # Salary must be positive — enforced at the database level
        CheckConstraint("salary > 0", name="ck_employee_salary_positive"),
        # Composite index for the most common analytics query:
        # "avg salary for job_title X in country Y"
        Index("idx_employee_country_job_title", "country", "job_title"),
    )

    def __repr__(self) -> str:
        return (
            f"<Employee id={self.id} name='{self.full_name}' "
            f"country='{self.country}' salary={self.salary}>"
        )
