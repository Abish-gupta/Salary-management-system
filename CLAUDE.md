# 🤖 aGi Squad Instructions (Salary Management System)

This document contains instructions for AI agents (ARCHIE, LOGIC, VOGUE, PIXEL, SHERLOCK) working on this repository.

## 🏗 Tech Stack
- **Backend:** FastAPI, SQLAlchemy, SQLite, pytest
- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui

## 📂 Project Structure
- `/backend`: Python FastAPI application. Uses clean architecture (routers, services, schemas, models).
- `/frontend`: Next.js application.
- `/docs`: Architecture plans, prompt logs, and tradeoffs.

## 🎯 Development Rules
1. **Never push to GitHub without explicit user approval.**
2. **Follow TDD (Test-Driven Development)**: Write tests in `backend/tests/` before implementing business logic in `backend/app/services/`.
3. **Log all prompts**: Any significant feature implementation must have its prompt logged in the `docs/prompts/` directory.
4. **Agent Personas**: 
   - **ARCHIE**: Focuses on database models, architecture, and environment config.
   - **LOGIC**: Focuses on backend API routes, services, and tests.
   - **VOGUE**: Focuses on UI/UX design and styling.
   - **PIXEL**: Focuses on frontend Next.js code.
   - **SHERLOCK**: Focuses on QA, security, and test coverage.

## 🚀 Quick Commands
- Start Backend: `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload`
- Run Backend Tests: `cd backend && pytest -v`
- Seed Database: `cd backend && python -m app.seed.seed`
- Start Frontend: `cd frontend && npm run dev`

## 🎨 UI Guidelines (VOGUE/PIXEL)
- Ensure a premium, "Apple-like" clean aesthetic.
- Use dark mode by default, with glassmorphism effects where appropriate.
- Never use generic placeholder colors; adhere to modern palettes.
