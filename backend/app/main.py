"""FastAPI application entry point.

This module creates and configures the FastAPI application instance.
Routes and middleware are registered here.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Salary Management API",
    description="API for managing employee salaries and generating analytics insights.",
    version="0.1.0",
)

# CORS middleware — allows the Next.js frontend to communicate with the API.
# In production, restrict origins to the actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Health check endpoint for monitoring and deployment readiness probes."""
    return {"status": "healthy"}
