# Design Tradeoffs

This document explains key engineering decisions and their tradeoffs.

## 1. SQLite vs PostgreSQL

**Chosen: SQLite**

| Factor | SQLite | PostgreSQL |
|--------|--------|-----------|
| Setup complexity | Zero-config | Requires server |
| Performance at 10K rows | Excellent | Overkill |
| Deployment | Single file | Managed service |
| Concurrent writes | Limited | Excellent |
| Assessment alignment | Explicitly suggested | Not mentioned |

**Tradeoff**: We sacrifice write concurrency for simplicity. For a single-user HR tool with 10K records, SQLite is the pragmatic choice. If this needed multi-user concurrent access, PostgreSQL would be necessary.

## 2. Service Layer vs Direct ORM in Routes

**Chosen: Separate service layer**

**Pro**: Business logic is testable without HTTP. We can write fast unit tests against services using just a database session.

**Con**: Adds a layer of indirection. For a small app, some might argue this is over-engineering.

**Rationale**: The assessment values "good code structure, readability, and maintainability." The service layer demonstrates clean architecture thinking, which outweighs the minor complexity cost.

## 3. Bulk Insert vs Individual Inserts (Seeding)

**Chosen: `executemany()` with raw SQL values**

**Tradeoff**: We bypass ORM event hooks (e.g., `before_insert`) for speed. This is acceptable for seed data where we control all inputs. The assessment explicitly says "performance of the script matters."

**Expected performance**: < 3 seconds for 10K records.

## 4. In-Memory SQLite for Tests

**Chosen: `sqlite:///:memory:`**

**Pro**: Tests run in ~100ms. No file I/O. No cleanup needed. Complete isolation.

**Con**: Slightly different behavior than file-based SQLite (e.g., foreign key enforcement). Mitigated by enabling foreign keys explicitly in test config.

## 5. Next.js App Router vs Pages Router

**Chosen: App Router (Next.js 14)**

**Pro**: Modern approach, server components for performance, cleaner layouts.

**Con**: Slightly newer API surface, fewer community examples.

**Rationale**: For a greenfield project in 2026, App Router is the standard choice.

## 6. shadcn/ui vs Material UI vs Ant Design

**Chosen: shadcn/ui**

**Pro**: Copy-paste ownership (no npm dependency), built on Radix UI (accessible), Tailwind-native, beautiful defaults.

**Con**: Manual component installation, less out-of-box complexity than Ant Design.

**Rationale**: For an assessment that values "code quality," owning the component code is better than hiding behind a heavy framework.
