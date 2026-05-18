# Salary Management System — Implementation Plan v2

## Goal

Build a minimal yet production-quality salary management tool for an HR Manager persona managing 10,000 employees. The system must support Employee CRUD, salary analytics by country/job-title, bulk seeding, and be fully deployed with a video demo.

**GitHub Repo**: https://github.com/Abish-gupta/Salary-management-system.git

---

## Assessment Requirements Summary

| # | Requirement | Priority |
|---|-------------|----------|
| 1 | Employee CRUD (Add, View, Update, Delete) via UI | **Must** |
| 2 | Employee fields: full name, job title, country, salary + extras | **Must** |
| 3 | Min/Max/Avg salary by country | **Must** |
| 4 | Avg salary by job title in a country | **Must** |
| 5 | Additional meaningful metrics | **Should** |
| 6 | Seed script for 10,000 employees (performant, uses name files) | **Must** |
| 7 | Unit tests (fast, deterministic, readable) | **Must** |
| 8 | Deployed + Video demo | **Must** |
| 9 | Incremental commits showing evolution | **Must** |
| 10 | Artifacts (planning notes, architecture, prompts, tradeoffs) | **Must** |

---

## Multi-Agent Workflow Strategy

> [!IMPORTANT]
> **How we'll use the aGi Agent Squad with Antigravity:**
>
> Antigravity runs as a single agent session, but we simulate the **aGi Squad** by explicitly routing each task to the right "agent persona" within the same conversation. Each commit will be tagged with the agent that handled it.

### Agent Assignments

| Agent | Responsibility | Commits |
|-------|---------------|---------|
| **ARCHIE** | Project init, DB model, config, architecture docs | Commits 1-2 |
| **LOGIC** | Backend services, API routes, seed script, tests | Commits 3-6 |
| **VOGUE** | UI/UX design specs, color palette, layout plan | Commit 7 (design phase) |
| **PIXEL** | Frontend implementation (Next.js + shadcn/ui) | Commits 7-8 |
| **SHERLOCK** | Final QA, security audit, test coverage review | Commit 9 |

### Frontend in a Separate Session

For the frontend (Phase 7-8), you can open a **second Antigravity conversation** in your workspace. Here's the workflow:

```
Session 1 (This one) → Backend (ARCHIE + LOGIC)
  ├── Commits 1-6: Backend complete with tests
  ├── Push to GitHub after each commit (with your approval)
  └── Backend deployed

Session 2 (New conversation) → Frontend (VOGUE + PIXEL)
  ├── Pull latest from GitHub
  ├── Commits 7-8: Frontend complete
  └── Frontend deployed
```

**Git workflow for multi-session:**
1. Session 1 pushes backend commits to `main` branch on GitHub
2. Session 2 clones/pulls the repo, builds frontend on top
3. Both sessions commit to the same GitHub repo
4. You approve every push in both sessions

> [!TIP]
> You can also do everything in this single session if you prefer — the multi-session approach is optional and mainly useful if you want to parallelize the work.

---

## Architecture Decisions

### Backend: FastAPI + SQLAlchemy + SQLite

**Why FastAPI?**
- Auto-generated OpenAPI docs (Swagger UI) — great for demo
- Async-capable, lightweight, fast
- Pydantic for data validation out of the box
- Python typing is first-class

**Why SQLite?**
- Zero-config, no external DB server needed
- Perfect for 10K records (well within SQLite's sweet spot)
- Single-file DB simplifies deployment and demo
- Assessment explicitly suggests SQLite

**Why SQLAlchemy?**
- Industry-standard ORM for Python
- Clean separation of models from business logic
- Migration support via Alembic (if needed later)
- Type-safe queries

### Frontend: Next.js 14 + TypeScript + Tailwind + shadcn/ui

**Why Next.js?** Assessment explicitly lists it as an option.

**Why shadcn/ui?** Production-grade, accessible, beautiful defaults, Tailwind-native.

**UI Vision**: Modern, aesthetic, premium feel. Think clean dashboards with glassmorphism, smooth animations, proper dark mode, and data visualization that impresses. NOT a basic CRUD form.

---

## Project Structure

```
salary-management/
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Settings & environment config
│   │   ├── database.py          # SQLAlchemy engine & session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── employee.py      # Employee SQLAlchemy model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── employee.py      # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── employee_service.py   # Business logic (CRUD)
│   │   │   └── analytics_service.py  # Salary analytics logic
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── employees.py     # Employee CRUD endpoints
│   │   │   └── analytics.py     # Analytics endpoints
│   │   └── seed/
│   │       ├── __init__.py
│   │       ├── seed.py          # Seed script entry point
│   │       ├── first_names.txt
│   │       └── last_names.txt
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Shared fixtures (test DB)
│   │   ├── test_employee_service.py
│   │   ├── test_analytics_service.py
│   │   ├── test_employee_router.py
│   │   └── test_seed.py
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── README.md
│
├── frontend/                    # Next.js application
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx         # Dashboard / Landing
│   │   │   ├── employees/
│   │   │   │   └── page.tsx     # Employee list + CRUD
│   │   │   └── analytics/
│   │   │       └── page.tsx     # Salary insights
│   │   ├── components/
│   │   │   ├── ui/              # shadcn components
│   │   │   ├── layout/
│   │   │   ├── employees/
│   │   │   └── analytics/
│   │   ├── lib/
│   │   │   ├── api.ts           # API client (fetch wrapper)
│   │   │   ├── types.ts         # Shared TypeScript types
│   │   │   └── utils.ts         # Formatting helpers
│   │   └── hooks/
│   │       └── use-employees.ts # Data fetching hooks
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
│
├── docs/                        # Assessment artifacts
│   ├── architecture.md          # Architecture overview
│   ├── development-log.md       # Step-by-step AI collaboration log
│   ├── tradeoffs.md             # Design decisions & tradeoffs
│   └── prompts/                 # AI prompts used (every prompt logged)
│       ├── 00-initial-planning.md
│       ├── 01-project-init.md
│       ├── 02-database-model.md
│       └── ...
│
├── .gitignore
└── README.md                    # Project overview + setup guide
```

---

## Data Model

### Employee Table

| Column | Type | Constraints | Rationale |
|--------|------|-------------|-----------|
| `id` | INTEGER | PK, AUTOINCREMENT | Standard surrogate key |
| `full_name` | VARCHAR(200) | NOT NULL | Assessment requirement |
| `email` | VARCHAR(254) | UNIQUE, NOT NULL | Realistic HR data |
| `job_title` | VARCHAR(100) | NOT NULL, INDEXED | Analytics filter field |
| `department` | VARCHAR(100) | NOT NULL | Meaningful HR field |
| `country` | VARCHAR(100) | NOT NULL, INDEXED | Analytics filter field |
| `salary` | DECIMAL(12,2) | NOT NULL, CHECK > 0 | Core analytics field |
| `currency` | VARCHAR(3) | NOT NULL, DEFAULT 'USD' | Multi-country context |
| `hire_date` | DATE | NOT NULL | Tenure analysis |
| `created_at` | DATETIME | NOT NULL, DEFAULT NOW | Audit trail |
| `updated_at` | DATETIME | NOT NULL, DEFAULT NOW | Audit trail |

### Indexes
- `idx_employee_country` — for country-based analytics
- `idx_employee_job_title` — for job-title analytics
- `idx_employee_country_job_title` — for combined queries

---

## Commit-by-Commit Plan

> [!IMPORTANT]
> **Rules:**
> 1. I will NOT push to GitHub without your explicit approval
> 2. Each commit is reviewed by you before push
> 3. Every AI prompt used is saved in `docs/prompts/`
> 4. Development log is updated after each commit

---

### Commit 1 — Project Scaffolding
**Agent**: ARCHIE  
**What**: Initialize repo, create folder structure, `.gitignore`, `README.md`, backend project config (`pyproject.toml`, `requirements.txt`), docs folder with architecture & tradeoffs, initial prompt log  
**Why**: Establishes the foundation. Assessment reviewers see clean project structure from the first commit.  
**Files created**: ~15 files (structure + config + docs)  
**Tests**: None (no logic yet)  
**Commit message**: `chore: initialize project with backend scaffolding and architecture docs`

---

### Commit 2 — Database Model & Config
**Agent**: ARCHIE  
**What**: Employee SQLAlchemy model with constraints & indexes, database engine/session setup, Pydantic schemas (Create, Update, Response), config module  
**Why**: Data layer must exist before any business logic. Schema design drives everything.  
**Files created**: `database.py`, `models/employee.py`, `schemas/employee.py`, `config.py`  
**Tests**: None (model-only, tested implicitly in Commit 3)  
**Commit message**: `feat: add employee model, database config, and pydantic schemas`

---

### Commit 3 — Employee CRUD Service + Tests
**Agent**: LOGIC  
**What**: `employee_service.py` (create, get_by_id, list with pagination/filters, update, delete), comprehensive unit tests  
**Why**: Service layer is the core business logic. Tests here are the most valuable — fast, deterministic, no HTTP overhead.  
**Files created**: `services/employee_service.py`, `tests/conftest.py`, `tests/test_employee_service.py`  
**Tests**: ~12-15 test cases covering happy path, edge cases, not-found, duplicates  
**Commit message**: `feat: implement employee CRUD service with unit tests`

---

### Commit 4 — Employee API Routes + Tests
**Agent**: LOGIC  
**What**: FastAPI router for `/api/employees` (GET list, GET by id, POST, PUT, DELETE), wire service to routes, API integration tests  
**Why**: Thin HTTP layer on top of services. Tests validate status codes, validation, response shapes.  
**Files created**: `routers/employees.py`, `tests/test_employee_router.py`  
**Tests**: ~10 API test cases  
**Commit message**: `feat: add employee CRUD API endpoints with integration tests`

---

### Commit 5 — Analytics Service + API + Tests
**Agent**: LOGIC  
**What**: `analytics_service.py` (country stats, job-title stats, department distribution, top earners), `/api/analytics` routes, tests  
**Why**: Core assessment requirement — salary insights.  
**Files created**: `services/analytics_service.py`, `routers/analytics.py`, `tests/test_analytics_service.py`  
**Tests**: ~8-10 analytics test cases  
**Commit message**: `feat: add salary analytics service and API with tests`

---

### Commit 6 — Seed Script
**Agent**: LOGIC  
**What**: `first_names.txt` + `last_names.txt` (200+ names each), performant seed script using bulk inserts, performance test  
**Why**: Assessment says "performance matters" for seeding. Target: < 3 seconds for 10K.  
**Files created**: `seed/seed.py`, `seed/first_names.txt`, `seed/last_names.txt`, `tests/test_seed.py`  
**Tests**: Seed count validation, performance benchmark  
**Commit message**: `feat: add performant 10K employee seed script`

---

### Commit 7 — Frontend: Employee Management UI
**Agent**: VOGUE (design spec) → PIXEL (implementation)  
**What**: Next.js app with modern aesthetic dashboard, employee table with search/filter/pagination, add/edit/delete dialogs, loading/error states  
**Why**: Core CRUD UI requirement. Must look premium.  
**UI Style**: Dark mode, glassmorphism cards, smooth transitions, Inter/Geist font, curated color palette  
**Files created**: ~15-20 frontend files  
**Tests**: N/A (manual verification via browser)  
**Commit message**: `feat: implement employee management UI with modern aesthetic design`

---

### Commit 8 — Frontend: Analytics Dashboard
**Agent**: PIXEL  
**What**: Analytics page with salary charts (Recharts), country selector, job-title breakdown, summary cards with animations  
**Why**: Core analytics requirement. Visual data presentation for HR persona.  
**Files created**: ~8-10 analytics components  
**Tests**: N/A (manual verification)  
**Commit message**: `feat: add salary analytics dashboard with interactive charts`

---

### Commit 9 — Polish, QA & Deploy
**Agent**: SHERLOCK (QA) → ARCHIE (deploy)  
**What**: Security audit, responsive design fixes, deployment config, final documentation, prompt logs  
**Why**: Assessment requires deployed + functional software.  
**Deployment**: Render (backend) + Vercel (frontend)  
**Commit message**: `chore: deploy application and finalize documentation`

---

### Commit 10 — Knowledge Graph (Bonus)
**Agent**: ARCHIE  
**What**: Run `/graphify` on the completed codebase to generate a knowledge graph. Commit the `GRAPH_REPORT.md` and `graph.html` to `docs/`.  
**Why**: Demonstrates advanced AI-assisted understanding of the codebase. Shows the assessment reviewers the interconnections between modules.  
**Commit message**: `docs: add codebase knowledge graph via graphify`

---

## Prompt Logging Strategy

Every AI prompt used during development will be saved in `docs/prompts/`:

```
docs/prompts/
├── 00-initial-planning.md      # The initial architecture prompt
├── 01-project-init.md          # Scaffolding prompt
├── 02-database-model.md        # Data model prompt
├── 03-crud-service.md          # Service layer prompt
├── 04-api-routes.md            # Routes prompt
├── 05-analytics.md             # Analytics prompt
├── 06-seed-script.md           # Seed script prompt
├── 07-frontend-ui.md           # UI design + implementation prompt
├── 08-analytics-dashboard.md   # Dashboard prompt
└── 09-deploy-polish.md         # Deployment prompt
```

Each file will contain:
- The exact prompt/instruction given
- Key decisions made by the AI
- Any manual corrections applied

---

## GitHub Push Workflow

```
For each commit:
1. I generate the code
2. You review it
3. I stage + commit locally with proper message
4. I ASK you: "Ready to push Commit N to GitHub?"
5. You say YES → I push
6. You say NO → We fix first
```

> [!CAUTION]
> I will NEVER push to GitHub without your explicit "yes".

---

## Testing Strategy

### Backend Tests
| Layer | What We Test | Tool |
|-------|-------------|------|
| Service | Business logic (CRUD, analytics) | pytest |
| Router | HTTP status codes, validation, response shapes | pytest + httpx TestClient |
| Seed | Correct count, name generation, performance | pytest |

### Test Database
- In-memory SQLite (`sqlite:///:memory:`) for tests
- Create/drop tables per test session
- No external dependencies

---

## Deployment Plan

| Component | Platform | Why |
|-----------|----------|-----|
| Backend | **Render** (free tier) | Simple Python deployment |
| Frontend | **Vercel** | Native Next.js support |
| Database | SQLite file (bundled) | Zero-config for demo |

---

## Verification Plan

### Automated Tests
```bash
cd backend && pytest -v --tb=short
```

### Manual Verification
- [ ] All CRUD operations work via UI
- [ ] Analytics display correctly for seeded data
- [ ] Responsive layout works on mobile
- [ ] Deployed URLs are accessible

### Knowledge Graph (Post-build)
- [ ] Run `/graphify` on completed codebase
- [ ] Review GRAPH_REPORT.md for architecture insights
- [ ] Commit graph artifacts to docs/
