/* eslint-disable @typescript-eslint/no-explicit-any */
/**
 * API Client for interacting with the Python FastAPI Backend.
 * Uses native fetch API.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface Employee {
  id: number;
  full_name: string;
  email: string;
  job_title: string;
  department: string;
  country: string;
  salary: number;
  hire_date: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export const api = {
  // --- Employee Endpoints ---
  async getEmployees(skip = 0, limit = 10, search = ''): Promise<PaginatedResponse<Employee>> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
      ...(search ? { search } : {})
    });
    
    const res = await fetch(`${API_BASE_URL}/employees?${params.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch employees');
    return res.json();
  },

  async createEmployee(data: Partial<Employee>): Promise<Employee> {
    const res = await fetch(`${API_BASE_URL}/employees`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to create employee');
    return res.json();
  },

  async updateEmployee(id: number, data: Partial<Employee>): Promise<Employee> {
    const res = await fetch(`${API_BASE_URL}/employees/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update employee');
    return res.json();
  },

  async deleteEmployee(id: number): Promise<void> {
    const res = await fetch(`${API_BASE_URL}/employees/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete employee');
  },

  // --- Analytics Endpoints ---
  async getGlobalStats(): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/analytics/global`);
    if (!res.ok) throw new Error('Failed to fetch global analytics');
    return res.json();
  },

  async getCountryStats(): Promise<any[]> {
    const res = await fetch(`${API_BASE_URL}/analytics/country`);
    if (!res.ok) throw new Error('Failed to fetch country analytics');
    return res.json();
  },

  async getSpecificCountryAnalytics(countryName: string): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/analytics/country/${encodeURIComponent(countryName)}`);
    if (!res.ok) throw new Error('Failed to fetch specific country analytics');
    return res.json();
  },

  async getDepartmentStats(): Promise<any[]> {
    const res = await fetch(`${API_BASE_URL}/analytics/department`);
    if (!res.ok) throw new Error('Failed to fetch department analytics');
    return res.json();
  }
};
