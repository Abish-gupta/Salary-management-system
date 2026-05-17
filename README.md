# Salary Management System

A minimal yet production-quality salary management tool for an organization with 10,000 employees. Built for the **HR Manager** persona.

## Features

- **Employee Management** — Add, view, update, and delete employees
- **Salary Insights** — Min/max/avg salary by country, avg salary by job title per country
- **Bulk Seeding** — Performant seed script for 10,000 employees
- **Analytics Dashboard** — Visual salary distribution and workforce metrics

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy, SQLite |
| Frontend | Next.js 14, TypeScript, Tailwind CSS, shadcn/ui |
| Testing | pytest (backend), vitest (frontend) |

## Project Structure

```
├── backend/          # FastAPI application
├── frontend/         # Next.js application
├── docs/             # Architecture & development artifacts
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or pnpm

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run seed script (10K employees)
python -m app.seed.seed

# Start the server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Running Tests

```bash
# Backend tests
cd backend && pytest -v

# Frontend tests
cd frontend && npm test
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Development Approach

This project was built incrementally with AI-assisted development, following:
- Test-driven development (TDD)
- Clean architecture with separation of concerns
- Incremental commits showing evolution
- Documented architectural decisions

See [`docs/`](./docs/) for detailed artifacts including architecture plans, development logs, and tradeoff explanations.

## License

MIT
