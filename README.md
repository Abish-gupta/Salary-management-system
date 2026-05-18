# 🏢 Salary Management System

![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwind-css)

A minimal, production-ready salary management tool designed for an HR Manager to effortlessly manage an organization of 10,000 employees. Built with a focus on performance, clean architecture, and a premium user experience.

🔗 **[Live Dashboard](https://salary-management-system-gamma.vercel.app)**  
🎥 **[Watch the Video Demo](https://youtu.be/HxRR9Fmynpw)**

---

## ✨ Features

- **👥 Employee Management:** Add, view, update, and delete employees with a smooth, intuitive interface.
- **📊 Advanced Salary Insights:** Instantly view minimum, maximum, and average salaries grouped by country.
- **💼 Job Title Analytics:** Drill down into average salaries by job title within specific countries.
- **🚀 High-Performance Seeding:** A blazingly fast bulk seed script capable of generating 10,000 realistic employee records in seconds.
- **🎨 Premium UI/UX:** A modern dashboard featuring glassmorphism, responsive charts, and a sleek dark mode.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, Recharts |
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy, SQLite |
| **Testing** | pytest (backend), vitest (frontend) |

---

## 🚀 Getting Started

Follow these simple steps to run the project locally.

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**

### 1. Backend Setup (API & Database)

Open your terminal and navigate to the backend folder:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt

# Seed the database with 10,000 employees
python -m app.seed.seed

# Start the server
uvicorn app.main:app --reload --port 8000
```
*The API will be available at `http://localhost:8000`. You can view the interactive documentation at `http://localhost:8000/docs`.*

### 2. Frontend Setup (Dashboard UI)

Open a new terminal window and navigate to the frontend folder:

```bash
cd frontend
npm install
npm run dev
```
*The dashboard will be available at `http://localhost:3000`.*

---

## 🧪 Running Tests

Ensure everything is working correctly by running the test suites.

**Backend Tests:**
```bash
cd backend
pytest -v
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

---

## 🏗 Architecture & Documentation

This project was built incrementally using **Test-Driven Development (TDD)** and clean architecture principles. 

For a deep dive into the development process, architectural decisions, and AI prompts used, please check out the [`docs/`](./docs/) directory.

---

