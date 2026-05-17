# Prompt 00 — Initial Planning & Architecture

**Date**: 2026-05-17  
**Agent**: ARCHIE  
**Purpose**: Analyze the assessment requirements and create a comprehensive architecture plan

---

## Prompt Given to AI

```
You are acting as a senior staff software engineer and AI pair programmer.

Your job is NOT to generate large amounts of code blindly.
Your job is to help me incrementally build a production-quality salary management 
system while following strong engineering principles, clean architecture, TDD, 
maintainability, and iterative software development.

We are following a development style inspired by:
- Andrej Karpathy-style AI-assisted software engineering
- incremental commits
- decomposition of problems
- test-driven thinking
- human-reviewed AI collaboration

# Tech Stack
Backend: FastAPI, SQLite, SQLAlchemy, Pytest
Frontend: Next.js, TypeScript, TailwindCSS, shadcn/ui

# Project Goal
Build a minimal but production-quality salary management system for 10,000 employees.

Core requirements:
- Employee CRUD
- Salary analytics
- Country-based salary insights
- Job-title salary insights
- Bulk employee seeding
- Unit tests
- Maintainable architecture
- Deployable application
```

## Key AI Decisions

1. **Chose service-layer architecture** over direct ORM-in-routes — enables testing business logic without HTTP overhead
2. **Proposed 11-column Employee model** — added `email`, `department`, `hire_date`, `currency` beyond minimum requirements for realistic HR data
3. **Recommended composite index** `(country, job_title)` for analytics queries
4. **Designed 10-commit plan** — each commit has a clear boundary and purpose
5. **Chose in-memory SQLite for tests** — fastest option, complete isolation

## Manual Corrections Applied

- User requested commit-by-commit plan with GitHub push approval at each step
- User requested all AI prompts be logged in `docs/prompts/`
- User requested modern/aesthetic UI design (not just functional)
- User added graphify knowledge graph as a bonus commit
