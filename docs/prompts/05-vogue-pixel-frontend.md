# Prompt 05 — VOGUE + PIXEL: Frontend UI (Commits F1–F3)

**Date**: 2026-05-17  
**Agent**: VOGUE (Design) → PIXEL (Implementation)  
**Branch**: `feature/frontend`

---

## VOGUE Sub-Agent Task Prompt (Design Phase)

```
You are VOGUE, the UI/UX Design agent in the aGi squad.

Task: Create a design specification for a salary management system frontend.

The user persona is: HR Manager — needs clear data, professional feel, minimal learning curve.

## Design Requirements

### Color Palette (Dark Mode)
Primary background:   #0F1117  (deep slate black)
Surface/cards:        #1A1D27  (dark navy)
Border:               #2D3148  (subtle separator)
Primary accent:       #6366F1  (indigo-500 — actions, highlights)
Secondary accent:     #8B5CF6  (violet-500 — charts, badges)
Success:              #10B981  (emerald — positive trends)
Warning:              #F59E0B  (amber — alerts)
Destructive:          #EF4444  (red — delete)
Text primary:         #F1F5F9  (slate-100)
Text muted:           #94A3B8  (slate-400)

### Typography
Font: Geist Sans (Next.js default) or Inter as fallback
Headings: font-semibold, tracking-tight
Body: font-normal, leading-relaxed
Monospace (salary figures): font-mono, tabular-nums

### Component Style
Cards: glassmorphism (backdrop-blur, semi-transparent backgrounds)
Buttons: rounded-lg, subtle hover transitions (200ms)
Tables: zebra striping with hover highlight
Inputs: dark background, indigo focus ring
Badges: rounded-full, color-coded by category

### Layout
Sidebar: 240px fixed, collapsible on mobile
Top header: 64px, breadcrumb + user info
Main content: fluid width, max-w-7xl, p-6 padding
Analytics cards: 3-column grid on desktop, 1-column on mobile

### Pages
1. /employees — Employee table with search/filter bar
2. /analytics  — Dashboard with stat cards + charts

### Animation
- Sidebar: slide-in on mobile
- Cards: fade-in-up on mount (staggered 100ms delay)
- Stat numbers: count-up animation on enter
- Table rows: fade on load

Produce a detailed text mockup (ASCII art) of each page layout.
```

---

## PIXEL Sub-Agent Task Prompt (Implementation Phase)

```
You are PIXEL, the Frontend Artist agent in the aGi squad.

Task: Implement the salary management system frontend in Next.js 14.

## Setup (Commit F1)
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir
cd frontend && npx shadcn@latest init

Install additional deps:
  npm install recharts lucide-react @tanstack/react-table

## Design System
Apply VOGUE's design specification:
- Global CSS variables in app/globals.css for all color tokens
- Dark mode by default (no theme toggle needed)
- Geist/Inter font

## Commit F1: Layout + Setup
Components to build:
  - components/layout/sidebar.tsx (nav links: Dashboard, Employees, Analytics)
  - components/layout/header.tsx (page title + user badge)
  - app/layout.tsx (sidebar + header wrapper)

## Commit F2: Employee Management UI
Pages/components:
  - app/employees/page.tsx (main employee page)
  - components/employees/employee-table.tsx
    - TanStack Table for sorting, column visibility
    - Pagination controls
    - Search bar (debounced 300ms)
    - Country/job-title filter dropdowns
  - components/employees/employee-form.tsx (shadcn Dialog/Sheet)
    - Add employee form (POST /api/employees)
    - Edit employee form (PUT /api/employees/{id})
    - Form validation via react-hook-form + zod
  - components/employees/delete-dialog.tsx
    - Confirmation before delete
  - Loading skeleton (shadcn Skeleton)
  - Error state component

## Commit F3: Analytics Dashboard
Pages/components:
  - app/analytics/page.tsx
  - components/analytics/stat-card.tsx (min/max/avg salary)
  - components/analytics/country-selector.tsx (shadcn Select)
  - components/analytics/salary-bar-chart.tsx (Recharts BarChart)
  - components/analytics/job-title-chart.tsx (Recharts HorizontalBar)
  - components/analytics/department-pie.tsx (Recharts PieChart)
  - components/analytics/top-earners-table.tsx

## API Integration
lib/api.ts: typed fetch wrapper around http://localhost:8000
lib/types.ts: match exactly with backend Pydantic response schemas
hooks/use-employees.ts: data fetching with loading/error states

## Key Requirements
- All loading states must show skeleton UI (not spinners)
- All error states must show actionable error messages
- Responsive: works on 320px mobile to 1920px desktop
- No placeholder images or lorem ipsum — use realistic seeded data
- Table must support at least 10K rows via server-side pagination
```

---

## Design Rationale

1. **Dark mode by default** — data-heavy dashboards (HR tools, analytics) are easier to scan in dark mode. Reduces eye strain during long sessions.
2. **Indigo/violet accent** — professional but distinctive. Avoids generic blue that every enterprise tool uses.
3. **TanStack Table** — handles complex table features (sorting, filtering, column visibility) better than a custom implementation. Assessment values code quality, not reinventing the wheel.
4. **Server-side pagination** — 10K employees cannot be loaded client-side. All filtering/sorting goes through API query params.
5. **Recharts** — lightweight (~100KB), composable, works great with Tailwind color tokens.
