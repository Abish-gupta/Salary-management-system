"""FastAPI application entry point.

This module creates and configures the FastAPI application instance.
Routes and middleware are registered here.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_tables

# Import models so they are registered with Base.metadata before create_tables()
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler — runs setup on startup, teardown on shutdown."""
    create_tables()
    yield
    # Teardown (connection pool cleanup handled by SQLAlchemy automatically)


app = FastAPI(
    title="Salary Management API",
    description="API for managing employee salaries and generating analytics insights.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware — allows the Next.js frontend to communicate with the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



from app.routers import employees, analytics

@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Health check endpoint for monitoring and deployment readiness probes."""
    return {"status": "healthy"}

app.include_router(employees.router)
app.include_router(analytics.router)
